import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spbu_semarang.db')

SPBU_DATA = [
    ("SPBU Pertamina 34-44203", "Pertamina", "Jl. Pemuda No. 101, Semarang", -6.9765, 110.4167, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44101", "Pertamina", "Jl. Ahmad Yani KM 5, Semarang", -6.9880, 110.4320, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44204", "Pertamina", "Jl. Pandanaran No. 75, Semarang", -6.9730, 110.4185, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44202", "Pertamina", "Jl. Gatot Subroto No. 120, Semarang", -6.9800, 110.4360, "00:00", "23:59", 1),
    ("SPBU Pertamina 34-44206", "Pertamina", "Jl. Sriwijaya No. 45, Semarang", -6.9809, 110.4102, "00:00", "23:59", 1),
    ("SPBU Shell Pemuda", "Shell", "Jl. Pemuda No. 55, Semarang", -6.9782, 110.4153, "06:00", "22:00", 1),
    ("SPBU Shell Raden Patah", "Shell", "Jl. Raden Patah No. 10, Semarang", -6.9745, 110.4118, "06:00", "22:00", 1),
    ("SPBU Vivo Sudirman", "Vivo", "Jl. Jend. Sudirman No. 329, Semarang", -6.9831, 110.4172, "06:00", "22:00", 1),
    ("SPBU Vivo Majapahit", "Vivo", "Jl. Majapahit No. 180, Semarang", -6.9742, 110.4198, "06:00", "22:00", 1),
    ("SPBU Pertamina Bawen", "Pertamina", "Jl. Raya Semarang-Solo KM 9, Semarang", -6.9235, 110.3910, "00:00", "23:59", 1),
    ("SPBU Pertamina Sudirman", "Pertamina", "Jl. Jend. Soedirman No. 142, Semarang", -6.9942, 110.4287, "00:00", "23:59", 1),
    ("SPBU Pertamina Bendungan", "Pertamina", "Jl. Bendungan Sigmund No. 49, Semarang", -6.9417, 110.4178, "00:00", "23:59", 1),
    ("SPBU Shell Dr. Cipto", "Shell", "Jl. Dr. Cipto No. 27, Semarang", -6.9838, 110.4252, "06:00", "22:00", 1),
    ("SPBU Pertamina Katamso", "Pertamina", "Jl. Brigjen Katamso No. 88, Semarang", -6.9601, 110.4124, "00:00", "23:59", 1),
    ("SPBU Pertamina Tambakrejo", "Pertamina", "Jl. Arteri Tambakrejo No. 9, Semarang", -6.9211, 110.4259, "00:00", "23:59", 1),
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
