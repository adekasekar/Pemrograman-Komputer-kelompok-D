import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spbu_semarang.db')

SPBU_DATA = [
    ("SPBU Pertamina 34-50101", "Pertamina", "Jl. Pemuda No. 25, Semarang", -6.9810, 110.4189, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-50106", "Pertamina", "Jl. Dr. Cipto No. 27, Semarang", -6.9838, 110.4252, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44204", "Pertamina", "Jl. Pandanaran No. 75, Semarang", -6.9730, 110.4185, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44206", "Pertamina", "Jl. Sriwijaya No. 45, Semarang", -6.9809, 110.4102, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-50110", "Pertamina", "Jl. Jend. Sudirman No. 329, Semarang", -6.9831, 110.4172, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44101", "Pertamina", "Jl. Ahmad Yani KM 5, Semarang", -6.9880, 110.4320, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44202", "Pertamina", "Jl. Gatot Subroto No. 120, Semarang", -6.9858, 110.4347, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-50114", "Pertamina", "Jl. Gajah Mada No. 12, Semarang", -6.9820, 110.4132, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45201", "Pertamina", "Jl. Jend. Sudirman No. 28, Semarang Utara", -6.9928, 110.4233, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45203", "Pertamina", "Jl. Imam Bonjol No. 26, Semarang Utara", -6.9870, 110.4237, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45205", "Pertamina", "Jl. Perintis Kemerdekaan No. 123, Semarang Utara", -6.9872, 110.4039, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45209", "Pertamina", "Jl. Kaligawe Raya No. 102, Semarang Utara", -6.9644, 110.4546, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45001", "Pertamina", "Jl. Soekarno Hatta No. 185, Semarang Timur", -6.9829, 110.4475, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45002", "Pertamina", "Jl. Tlogosari Raya No. 54, Semarang Timur", -6.9865, 110.4550, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45009", "Pertamina", "Jl. Kaligawe Selatan No. 1, Semarang Timur", -6.9796, 110.4508, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45010", "Pertamina", "Jl. Ariodran No. 9, Semarang Timur", -6.9920, 110.4390, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45101", "Pertamina", "Jl. Achmad Yani No. 88, Semarang Selatan", -6.9960, 110.4356, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45107", "Pertamina", "Jl. Brigjen Katamso No. 88, Semarang Selatan", -6.9601, 110.4124, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45104", "Pertamina", "Jl. Raya Manyaran No. 47, Semarang Selatan", -6.9707, 110.3950, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45109", "Pertamina", "Jl. A. Yani KM 8, Semarang Selatan", -6.9948, 110.4364, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45301", "Pertamina", "Jl. MT Haryono No. 123, Pedurungan", -6.9865, 110.4695, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45304", "Pertamina", "Jl. Kaligawe No. 16, Pedurungan", -6.9755, 110.4702, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45306", "Pertamina", "Jl. Beringin No. 34, Pedurungan", -6.9682, 110.4681, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45307", "Pertamina", "Jl. Garuda No. 9, Pedurungan", -6.9780, 110.4740, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45401", "Pertamina", "Jl. Teknik No. 5, Banyumanik", -6.9652, 110.3968, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45402", "Pertamina", "Jl. Tlogosari Raya No. 84, Banyumanik", -6.9874, 110.4548, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45405", "Pertamina", "Jl. Sendangmulyo No. 75, Banyumanik", -6.9322, 110.4103, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45501", "Pertamina", "Jl. Prof. Soedarto No. 12, Tembalang", -6.9830, 110.3794, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45502", "Pertamina", "Jl. Villa Tembalang No. 40, Tembalang", -6.9285, 110.3965, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45601", "Pertamina", "Jl. Menoreh No. 60, Genuk", -6.9715, 110.4618, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45701", "Pertamina", "Jl. Ngaliyan No. 112, Ngaliyan", -6.9525, 110.4022, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-45801", "Pertamina", "Jl. Letjen Suprapto No. 12, Tugu", -6.9588, 110.4192, "00:00", "23:59", 1),
]

ZONA_DATA = [
    ("Jl. Pemuda", "Semarang Tengah", 5, -6.9810, 110.4150, 400),
    ("Jl. Pandanaran", "Semarang Tengah", 4, -6.9735, 110.4190, 300),
    ("Simpang Lima", "Semarang Tengah", 5, -6.9815, 110.4105, 500),
    ("Jl. Ahmad Yani", "Semarang Timur", 4, -6.9900, 110.4310, 450),
    ("Jl. Gatot Subroto", "Semarang Selatan", 4, -6.9860, 110.4345, 400),
    ("Jl. Jend. Sudirman", "Semarang Utara", 3, -6.9930, 110.4250, 350),
    ("Jl. MT Haryono", "Pedurungan", 4, -6.9865, 110.4695, 350),
    ("Jl. Dr. Cipto", "Semarang Tengah", 3, -6.9825, 110.4225, 300),
    ("Jl. Brigjen Katamso", "Semarang Selatan", 2, -6.9650, 110.4118, 300),
    ("Jl. Yos Sudarso", "Tanjung Mas", 3, -6.9588, 110.4217, 300),
]


def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE spbu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            brand TEXT NOT NULL,
            alamat TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            jam_buka TEXT NOT NULL,
            jam_tutup TEXT NOT NULL,
            status_aktif INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE zona_lalu_lintas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_zona TEXT NOT NULL,
            kecamatan TEXT NOT NULL,
            tingkat_kepadatan INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            radius_meter INTEGER NOT NULL
        )
    """)

    cursor.executemany(
        "INSERT INTO spbu (nama, brand, alamat, latitude, longitude, jam_buka, jam_tutup, status_aktif) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        SPBU_DATA
    )

    cursor.executemany(
        "INSERT INTO zona_lalu_lintas (nama_zona, kecamatan, tingkat_kepadatan, latitude, longitude, radius_meter) VALUES (?, ?, ?, ?, ?, ?)",
        ZONA_DATA
    )

    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")


if __name__ == '__main__':
    init_db()
