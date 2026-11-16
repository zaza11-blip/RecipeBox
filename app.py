
import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Lokasi folder proyek
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lokasi penyimpanan foto
app.config["UPLOAD_FOLDER"] = os.path.join(
    BASE_DIR, "static", "uploads"
)

# Lokasi database
DATABASE = os.path.join(BASE_DIR, "database.db")

# Kategori resep
KATEGORI = [
    "Makanan utama",
    "Minuman",
    "Dessert",
    "Camilan"
]

# Format foto yang diperbolehkan
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


# Menghubungkan ke database
def koneksi_database():
    return sqlite3.connect(DATABASE)


# Memeriksa format foto
def foto_diizinkan(nama_file):
    return (
        "." in nama_file
        and nama_file.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Membuat nama file foto yang unik
def simpan_foto(file_foto):
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    nama_asli = secure_filename(file_foto.filename)
    nama_unik = datetime.now().strftime("%Y%m%d%H%M%S%f")
    nama_foto = nama_unik + "_" + nama_asli

    lokasi_foto = os.path.join(
        app.config["UPLOAD_FOLDER"],
        nama_foto
    )

    file_foto.save(lokasi_foto)
    return nama_foto


# Menghapus foto dari folder uploads
def hapus_file_foto(nama_foto):
    if nama_foto:
        lokasi_foto = os.path.join(
            app.config["UPLOAD_FOLDER"],
            os.path.basename(nama_foto)
        )

        if os.path.isfile(lokasi_foto):
            os.remove(lokasi_foto)


# Membuat tabel resep
def buat_tabel():
    with koneksi_database() as koneksi:
        koneksi.execute("""
            CREATE TABLE IF NOT EXISTS resep (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_resep TEXT NOT NULL,
                kategori TEXT NOT NULL,
                deskripsi TEXT,
                bahan TEXT NOT NULL,
                langkah TEXT NOT NULL,
                waktu_masak INTEGER,
                foto TEXT,
                created_at TEXT
            )
        """)


# HALAMAN 1: DASHBOARD
@app.route("/")
def index():
    with koneksi_database() as koneksi:
        total_resep = koneksi.execute(
            "SELECT COUNT(*) FROM resep"
        ).fetchone()[0]

        total_kategori = koneksi.execute(
            "SELECT COUNT(DISTINCT kategori) FROM resep"
        ).fetchone()[0]

        resep_terbaru = koneksi.execute("""
            SELECT * FROM resep
            ORDER BY id DESC
            LIMIT 5
        """).fetchall()

    return render_template(
        "dashboard.html",
        total_resep=total_resep,
        total_kategori=total_kategori,
        total_terbaru=len(resep_terbaru),
        resep_terbaru=resep_terbaru
    )


# HALAMAN 2: SEMUA RESEP
@app.route("/resep")
def semua_resep():
    pencarian = request.args.get("q", "").strip()
    kategori_pilihan = request.args.get("kategori", "")

    query = "SELECT * FROM resep WHERE 1=1"
    parameter = []

    if pencarian:
        query += " AND nama_resep LIKE ?"
        parameter.append(f"%{pencarian}%")

    if kategori_pilihan in KATEGORI:
        query += " AND kategori = ?"
        parameter.append(kategori_pilihan)

    query += " ORDER BY id DESC"

    with koneksi_database() as koneksi:
        daftar_resep = koneksi.execute(
            query, parameter
        ).fetchall()

    return render_template(
        "semua_resep.html",
        daftar_resep=daftar_resep,
        pencarian=pencarian,
        kategori_pilihan=kategori_pilihan,
        kategori=KATEGORI
    )


# HALAMAN 3: TAMBAH RESEP
@app.route("/tambah-resep", methods=["GET", "POST"])
def tambah_resep():
    pesan_error = ""
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()

        nama_resep = request.form.get("nama_resep", "").strip()
        kategori = request.form.get("kategori", "")
        deskripsi = request.form.get("deskripsi", "").strip()
        bahan = request.form.get("bahan", "").strip()
        langkah = request.form.get("langkah", "").strip()
        waktu_masak = request.form.get("waktu_masak", "").strip()

        file_foto = request.files.get("foto")
        nama_foto = None

        if not nama_resep or not bahan or not langkah or not waktu_masak:
            pesan_error = "Nama, bahan, langkah, dan waktu memasak wajib diisi."

        elif kategori not in KATEGORI:
            pesan_error = "Silakan pilih kategori yang tersedia."

        elif not waktu_masak.isdigit() or int(waktu_masak) < 1:
            pesan_error = "Waktu memasak harus berupa angka minimal 1 menit."

        elif file_foto and file_foto.filename:
            if not foto_diizinkan(file_foto.filename):
                pesan_error = "Format foto harus PNG, JPG, JPEG, atau WEBP."

        if not pesan_error:
            if file_foto and file_foto.filename:
                nama_foto = simpan_foto(file_foto)

            with koneksi_database() as koneksi:
                koneksi.execute("""
                    INSERT INTO resep (
                        nama_resep,
                        kategori,
                        deskripsi,
                        bahan,
                        langkah,
                        waktu_masak,
                        foto,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    nama_resep,
                    kategori,
                    deskripsi,
                    bahan,
                    langkah,
                    int(waktu_masak),
                    nama_foto,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))

            return redirect(url_for("semua_resep"))

    return render_template(
        "tambah_resep.html",
        kategori=KATEGORI,
        pesan_error=pesan_error,
        mode_edit=False,
        resep=None,
        form_data=form_data,
        action=url_for("tambah_resep")
    )


# HALAMAN 4: DETAIL RESEP
@app.route("/resep/<int:id>")
def detail_resep(id):
    with koneksi_database() as koneksi:
        resep = koneksi.execute(
            "SELECT * FROM resep WHERE id = ?",
            (id,)
        ).fetchone()

    if resep is None:
        abort(404)

    return render_template(
        "detail_resep.html",
        resep=resep
    )


# FITUR EDIT RESEP
@app.route("/resep/<int:id>/edit", methods=["GET", "POST"])
def edit_resep(id):
    with koneksi_database() as koneksi:
        resep = koneksi.execute(
            "SELECT * FROM resep WHERE id = ?",
            (id,)
        ).fetchone()

    if resep is None:
        abort(404)

    pesan_error = ""
    form_data = {}

    if request.method == "POST":
        form_data = request.form.to_dict()

        nama_resep = request.form.get("nama_resep", "").strip()
        kategori = request.form.get("kategori", "")
        deskripsi = request.form.get("deskripsi", "").strip()
        bahan = request.form.get("bahan", "").strip()
        langkah = request.form.get("langkah", "").strip()
        waktu_masak = request.form.get("waktu_masak", "").strip()

        file_foto = request.files.get("foto")
        nama_foto = resep[7]

        if not nama_resep or not bahan or not langkah or not waktu_masak:
            pesan_error = "Nama, bahan, langkah, dan waktu memasak wajib diisi."

        elif kategori not in KATEGORI:
            pesan_error = "Silakan pilih kategori yang tersedia."

        elif not waktu_masak.isdigit() or int(waktu_masak) < 1:
            pesan_error = "Waktu memasak harus berupa angka minimal 1 menit."

        elif file_foto and file_foto.filename:
            if not foto_diizinkan(file_foto.filename):
                pesan_error = "Format foto harus PNG, JPG, JPEG, atau WEBP."

        if not pesan_error:
            if file_foto and file_foto.filename:
                nama_foto = simpan_foto(file_foto)

            with koneksi_database() as koneksi:
                koneksi.execute("""
                    UPDATE resep
                    SET nama_resep = ?,
                        kategori = ?,
                        deskripsi = ?,
                        bahan = ?,
                        langkah = ?,
                        waktu_masak = ?,
                        foto = ?
                    WHERE id = ?
                """, (
                    nama_resep,
                    kategori,
                    deskripsi,
                    bahan,
                    langkah,
                    int(waktu_masak),
                    nama_foto,
                    id
                ))

            if file_foto and file_foto.filename:
                hapus_file_foto(resep[7])

            return redirect(url_for("detail_resep", id=id))

    return render_template(
        "tambah_resep.html",
        kategori=KATEGORI,
        pesan_error=pesan_error,
        mode_edit=True,
        resep=resep,
        form_data=form_data,
        action=url_for("edit_resep", id=id)
    )


# FITUR HAPUS RESEP
@app.route("/resep/<int:id>/hapus", methods=["POST"])
def hapus_resep(id):
    with koneksi_database() as koneksi:
        resep = koneksi.execute(
            "SELECT foto FROM resep WHERE id = ?",
            (id,)
        ).fetchone()

        if resep is None:
            abort(404)

        koneksi.execute(
            "DELETE FROM resep WHERE id = ?",
            (id,)
        )

    hapus_file_foto(resep[0])

    return redirect(url_for("semua_resep"))


# HALAMAN 5: PENGATURAN
@app.route("/pengaturan")
def pengaturan():
    return render_template(
        "pengaturan.html",
        kategori=KATEGORI
    )


if __name__ == "__main__":
    buat_tabel()
    print("Database RecipeBox:", DATABASE)
    app.run(debug=True)
