# Pemrograman-Komputer-kelompok-D

Penentuan Lokasi SPBU Strategis di Kota Semarang Berdasarkan Aksesibilitas dan Kepadatan Lalu Lintas

## Struktur Project

- `app.py`
- `templates/`
  - `index.html`
- `static/`
  - `css/style.css`
  - `js/main.js`
- `database/`
- `requirements.txt`

## Setup dan Menjalankan di Localhost

1. Pastikan Python sudah terpasang.
2. Buka terminal di folder project ini.
3. Buat virtual environment (opsional):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install dependensi:
   ```powershell
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi:
   ```powershell
   python app.py
   ```
6. Buka browser dan akses:
   ```text
   http://127.0.0.1:5000
   ```

## Catatan

- Database SQLite akan menggunakan file `database/spbu_semarang.db`.
- Folder `templates/` menyimpan tampilan HTML.
- Folder `static/` menyimpan aset CSS dan JavaScript.
