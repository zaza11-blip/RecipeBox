\# 🍽️ RecipeBox



\*\*RecipeBox\*\* adalah aplikasi web untuk menyimpan dan mengelola koleksi resep makanan dan minuman. Aplikasi ini dibuat menggunakan Python dan Flask dengan database SQLite.



\## ✨ Fitur Utama



\- \*\*Dashboard:\*\* Menampilkan ringkasan jumlah resep dan kategori.

\- \*\*Tambah Resep:\*\* Menambahkan resep baru beserta foto.

\- \*\*Semua Resep:\*\* Melihat seluruh koleksi resep.

\- \*\*Pencarian:\*\* Mencari resep berdasarkan nama.

\- \*\*Filter Kategori:\*\* Mengelompokkan resep berdasarkan kategori.

\- \*\*Detail Resep:\*\* Melihat informasi lengkap resep.

\- \*\*Edit Resep:\*\* Mengubah informasi resep.

\- \*\*Hapus Resep:\*\* Menghapus resep yang tidak diperlukan.

\- \*\*Pengaturan:\*\* Menampilkan halaman pengaturan aplikasi.



\## 🛠️ Teknologi



\- Python

\- Flask

\- SQLite

\- HTML

\- CSS

\- Jinja2



\## 📂 Struktur Folder



```text

RecipeBox/

├── app.py

├── .gitignore

├── README.md

├── database.db

├── static/

│   ├── css/

│   │   └── style.css

│   └── uploads/

└── templates/

&#x20;   ├── dashboard.html

&#x20;   ├── semua\_resep.html

&#x20;   ├── tambah\_resep.html

&#x20;   ├── detail\_resep.html

&#x20;   └── pengaturan.html

```



\## 🚀 Cara Menjalankan



1\. Pastikan Python sudah terinstal.

2\. Clone repository ini:



```bash

git clone https://github.com/zaza11-blip/RecipeBox.git

```



3\. Masuk ke folder proyek:



```bash

cd RecipeBox

```



4\. Instal Flask:



```bash

pip install flask

```



5\. Jalankan aplikasi:



```bash

python app.py

```



6\. Buka browser dan kunjungi:



```text

http://127.0.0.1:5000

```



Database SQLite akan dibuat secara otomatis ketika aplikasi pertama kali dijalankan.



\## 📌 Kategori Resep



\- Makanan utama

\- Minuman

\- Dessert

\- Camilan



\---



\*\*RecipeBox — Your Personal Recipe Collection.\*\*

