import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'spbu_semarang.db')

SPBU_DATA = [
    ("Pertamina", "Pertamina", "-", "Tembalang", -7.111113, 110.397583, "00:00", "23:59"),
    ("Pertamina Sekaran", "Pertamina", "Jalan Sekaran Raya", "Gunungpati", -7.056014, 110.392381, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "-", "Pedurungan", -7.005721, 110.456119, "00:00", "23:59"),
    ("SPBU Pertamina", "Pertamina", "-", "Gunungpati", -7.096898, 110.381942, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "Jalan Arteri Utara", "Semarang Utara", -6.956407, 110.416406, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "-", "Pedurungan", -7.002080, 110.447876, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "-", "Ngaliyan", -7.039013, 110.330411, "00:00", "23:59"),
    ("SPBU 44.505.08", "Pertamina", "Jalan Diponegoro", "Gunungpati", -7.136430, 110.405321, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "-", "Gunungpati", -7.148149, 110.407796, "00:00", "23:59"),
    ("SPBU 44.501.12", "Pertamina", "Jalan Imam Bonjol No. 122-124", "Semarang Tengah", -6.974669, 110.413755, "00:00", "23:59"),
    ("SPBU 43.502.01", "Pertamina", "Jalan Lamper Tengah", "Semarang Selatan", -7.002998, 110.444180, "00:00", "23:59"),
    ("SPBU 44.505.09", "Pertamina", "-", "Gunungpati", -7.146145, 110.421847, "00:00", "23:59"),
    ("SPBU 44.502.01", "Pertamina", "Jalan Letjen S. Parman", "Gajahmungkur", -7.004337, 110.409390, "00:00", "23:59"),
    ("SPBU 41.502.02", "Pertamina", "Jalan Sisingamangaraja", "Candisari", -7.016011, 110.418820, "00:00", "23:59"),
    ("SPBU 44.501.19", "Pertamina", "Jalan Pamularsih", "Semarang Barat", -6.988651, 110.394170, "00:00", "23:59"),
    ("SPBU 41.502.14", "Pertamina", "Jalan Kaligarang No. 16", "Gajahmungkur", -6.996296, 110.404949, "00:00", "23:59"),
    ("SPBU 44.502.15", "Pertamina", "Jalan Menoreh Raya", "Gajahmungkur", -7.017572, 110.388830, "00:00", "23:59"),
    ("SPBU 44.501.40", "Pertamina", "Jalan Jendral Sudirman", "Semarang Barat", -6.980480, 110.399616, "00:00", "23:59"),
    ("SPBU 44.501.31", "Pertamina", "Jalan Gajah Raya", "Gayamsari", -6.994343, 110.446805, "00:00", "23:59"),
    ("SPBU 44.501.04", "Pertamina", "Jalan Majapahit No.150", "Gayamsari", -7.002114, 110.447815, "00:00", "23:59"),
    ("SPBU 44.501.21", "Pertamina", "Jalan Dr. Cipto No. 152", "Semarang Timur", -6.984611, 110.435222, "00:00", "23:59"),
    ("SPBU 44.501.37", "Pertamina", "Jalan Dr. Cipto No. 29", "Semarang Timur", -6.973969, 110.434172, "00:00", "23:59"),
    ("SPBU 44.502.07", "Pertamina", "Jalan Sriwijaya", "Candisari", -6.998324, 110.421020, "00:00", "23:59"),
    ("SPBU 44.501.18", "Pertamina", "Jalan Soekarno Hatta", "Gayamsari", -6.976732, 110.448341, "00:00", "23:59"),
    ("SPBU 41.502.01", "Pertamina", "Jalan Ahmad Yani No. 157-159", "Semarang Selatan", -6.992420, 110.426801, "00:00", "23:59"),
    ("SPBU 44.501.07", "Pertamina", "Jalan Yos Sudarso No. 6", "Semarang Utara", -6.969851, 110.391084, "00:00", "23:59"),
    ("SPBU 44.501.10", "Pertamina", "Jalan Imam Bonjol", "Semarang Tengah", -6.968881, 110.430618, "00:00", "23:59"),
    ("SPBU 44.501.22", "Pertamina", "Jalan Kelud Raya", "Gajahmungkur", -7.007197, 110.396375, "00:00", "23:59"),
    ("SPBU 44.501.16", "Pertamina", "Jalan Pengapon No. 2", "Semarang Utara", -6.962872, 110.433090, "00:00", "23:59"),
    ("SPBU 44.501.41", "Pertamina", "Jalan Pemuda No. 59-63", "Semarang Tengah", -6.974991, 110.418574, "00:00", "23:59"),
    ("SPBU 44.502.22", "Pertamina", "Jalan Dr. Wahidin", "Candisari", -7.017497, 110.427766, "00:00", "23:59"),
    ("SPBU 44.501.15", "Pertamina", "Jalan Majapahit No. 224", "Pedurungan", -7.005767, 110.456092, "00:00", "23:59"),
    ("SPBU 44.501.26", "Pertamina", "Jalan Soekarno Hatta", "Pedurungan", -6.988481, 110.455763, "00:00", "23:59"),
    ("SPBU 44.501.36", "Pertamina", "Jalan Kaligawe Raya", "Genuk", -6.957035, 110.457079, "00:00", "23:59"),
    ("SPBU 44.501.09", "Pertamina", "Jalan Siliwangi No. 440", "Semarang Barat", -6.985576, 110.381259, "00:00", "23:59"),
    ("SPBU Pertamina 44.501.39", "Pertamina", "Jalan Komdor Laut Yos Sudarso", "Semarang Utara", -6.952744, 110.451200, "00:00", "23:59"),
    ("SPBU 44.502.12", "Pertamina", "Jalan Perintis Kemerdekaan", "Banyumanik", -7.107706, 110.412319, "00:00", "23:59"),
    ("SPBU 44.502.23", "Pertamina", "Jalan Prof. Soedarto, Tembalang", "Tembalang", -7.054602, 110.432603, "00:00", "23:59"),
    ("SPBU 44.501.11", "Pertamina", "Jalan Raya Genuk", "Genuk", -6.953984, 110.473307, "00:00", "23:59"),
    ("SPBU 44.502.16", "Pertamina", "Jalan Imam Suparto", "Tembalang", -7.057322, 110.460700, "00:00", "23:59"),
    ("SPBU 44.502.03", "Pertamina", "Jalan Perintis Kemerdekaan No. 177", "Banyumanik", -7.099576, 110.408903, "00:00", "23:59"),
    ("SPBU 44.501.24", "Pertamina", "Jalan Indraprasta No. 20-22", "Semarang Tengah", -6.978436, 110.409638, "00:00", "23:59"),
    ("SPBU 44.501.20", "Pertamina", "Jalan Abdul Rachman Saleh", "Semarang Barat", -6.997716, 110.379475, "00:00", "23:59"),
    ("SPBU 44.502.24", "Pertamina", "Jalan Dukuh Kuncen, Mijen", "Mijen", -7.093165, 110.326142, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "-", "Gunungpati", -7.130325, 110.424208, "00:00", "23:59"),
    ("SPBU 44.501.25", "Pertamina", "Jalan Wolter Monginsidi No. 88b", "Genuk", -6.961532, 110.478489, "00:00", "23:59"),
    ("SPBU 44.501.30", "Pertamina", "Jalan Simongan", "Semarang Barat", -7.000176, 110.396712, "00:00", "23:59"),
    ("SPBU 44.502.19", "Pertamina", "Jalan Perintis Kemerdekaan", "Banyumanik", -7.080733, 110.411581, "00:00", "23:59"),
    ("SPBU 44.501.03", "Pertamina", "Jalan Kaligawe", "Genuk", -6.948026, 110.491047, "00:00", "23:59"),
    ("SPBU 44.501.03 Genuk", "Pertamina", "Jalan Raya Semarang-Demak", "Genuk", -6.950611, 110.483816, "00:00", "23:59"),
    ("SPBU 44.502.17", "Pertamina", "Jalan Boja, Jatisari", "Mijen", -7.062734, 110.310931, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "-", "Gunungpati", -7.130868, 110.409012, "00:00", "23:59"),
    ("SPBU 44.501.13", "Pertamina", "Jalan Prof. Dr. Hamka", "Ngaliyan", -6.990456, 110.355569, "00:00", "23:59"),
    ("SPBU 44.502.21", "Pertamina", "Jalan Muntal Raya, Patemon", "Gunungpati", -7.074190, 110.389842, "00:00", "23:59"),
    ("SPBU 44.501.23", "Pertamina", "Jalan Siliwangi No. 576 Krapyak", "Semarang Barat", -6.988202, 110.366244, "00:00", "23:59"),
    ("SPBU 44.501.32", "Pertamina", "Jalan Wolter Mongonsidi", "Pedurungan", -6.988810, 110.474093, "00:00", "23:59"),
    ("SPBU 44.501.29", "Pertamina", "Jalan Raya Semarang-Kendal KM 14", "Tugu", -6.972975, 110.314043, "00:00", "23:59"),
    ("SPBU 44.501.14", "Pertamina", "Jalan Raya Randugarut", "Tugu", -6.984849, 110.337909, "00:00", "23:59"),
    ("SPBU 41.501.28", "Pertamina", "Jalan Brigjen Sudiarto, Penggaron", "Pedurungan", -7.016484, 110.486822, "00:00", "23:59"),
    ("SPBU 44.501.27", "Pertamina", "Jalan Walisongo", "Ngaliyan", -6.979141, 110.333678, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "Jalan Ketileng Raya", "Pedurungan", -7.025166, 110.467645, "00:00", "23:59"),
    ("SPBU 44.502.25", "Pertamina", "Jalan Raya Gunungpati Manyaran", "Gunungpati", -7.084593, 110.361090, "00:00", "23:59"),
    ("SPBU 44.501.01", "Pertamina", "Jalan Brigjen Sudiarto KM 11", "Pedurungan", -7.019495, 110.493158, "00:00", "23:59"),
    ("Pertamina", "Pertamina", "Jalan Sarwo Edi Wibowo", "Pedurungan", -7.023102, 110.487622, "00:00", "23:59"),
    ("SPBU 44.502.04", "Pertamina", "Jalan Setiabudi, Gombel", "Banyumanik", -7.042884, 110.422320, "00:00", "23:59"),
    ("SPBU 44.502.02", "Pertamina", "Jalan Perintis Kemerdekaan No. 198", "Banyumanik", -7.064736, 110.412641, "00:00", "23:59"),
    ("SPBU 44.501.34", "Pertamina", "Jalan Brigjen Sudiarto", "Pedurungan", -7.014435, 110.480146, "00:00", "23:59"),
    ("SPBU 44.502.08", "Pertamina", "Jalan Kedungmundu No. 18", "Tembalang", -7.024145, 110.459845, "00:00", "23:59"),
    ("SPBU 44.502.20", "Pertamina", "Jalan Setia Budi No. 205, Srondol", "Banyumanik", -7.057880, 110.414349, "00:00", "23:59"),
    ("SPBU 44.502.11", "Pertamina", "Jalan Ngesrep Timur V", "Banyumanik", -7.051916, 110.427790, "00:00", "23:59"),
    ("SPBU 44.502.09", "Pertamina", "Jalan Raya Semarang-Boja", "Mijen", -7.028405, 110.334902, "00:00", "23:59"),
    ("SPBU 44.501.33", "Pertamina", "Jalan Untung Suropati Kav. 173", "Ngaliyan", -7.011836, 110.378587, "00:00", "23:59"),
    ("SPBU 44.501.18 Tugu", "Pertamina", "Jalan Semarang-Kendal", "Tugu", -6.974219, 110.301090, "00:00", "23:59"),
    ("SPBU Pertamina", "Pertamina", "-", "Semarang Timur", -6.959670, 110.444073, "00:00", "23:59"),
    ("SPBU Pertamina", "Pertamina", "-", "Tembalang", -7.064911, 110.470429, "00:00", "23:59"),
]

ZONA_DATA = [
    ("Jl. Pemuda", "Semarang Tengah", 5, -6.9923, 110.4178, 800),
    ("Simpang Lima", "Semarang Tengah", 5, -6.9934, 110.4123, 600),
    ("Jl. Pandanaran", "Semarang Tengah", 5, -6.9967, 110.4134, 700),
    ("Jl. Ahmad Yani", "Semarang Selatan", 5, -6.9924, 110.4268, 1000),
    ("Jl. Siliwangi", "Semarang Barat", 4, -6.9856, 110.3812, 1200),
    ("Jl. Jendral Sudirman", "Semarang Barat", 4, -6.9805, 110.3996, 900),
    ("Jl. Brigjen Sudiarto", "Pedurungan", 4, -7.0165, 110.4801, 1500),
    ("Jl. Kaligawe", "Genuk", 4, -6.9520, 110.4745, 1200),
    ("Jl. Majapahit", "Pedurungan", 4, -7.0021, 110.4478, 1000),
    ("Jl. Soekarno-Hatta", "Gayamsari", 4, -6.9767, 110.4483, 1100),
    ("Jl. Dr. Cipto", "Semarang Timur", 3, -6.9840, 110.4350, 700),
    ("Jl. Setia Budi", "Banyumanik", 3, -7.0429, 110.4223, 900),
    ("Jl. Prof. Soedarto", "Tembalang", 3, -7.0546, 110.4326, 800),
    ("Jl. Perintis Kemerdekaan", "Banyumanik", 3, -7.0648, 110.4126, 1000),
    ("Jl. Walisongo", "Ngaliyan", 3, -6.9791, 110.3337, 1100),
    ("Jl. Raya Kendal", "Tugu", 3, -6.9730, 110.3140, 1200),
    ("Jl. Raya Genuk", "Genuk", 3, -6.9540, 110.4730, 900),
    ("Jl. Kedungmundu", "Tembalang", 3, -7.0241, 110.4598, 800),
    ("Jl. Sisingamangaraja", "Candisari", 3, -7.0160, 110.4188, 600),
    ("Jl. Kaligarang", "Gajahmungkur", 3, -6.9963, 110.4049, 600),
    ("Jl. Fatmawati", "Tembalang", 2, -7.0389, 110.4456, 700),
    ("Jl. Raya Mijen", "Mijen", 2, -7.0284, 110.3349, 800),
    ("Jl. Raya Gunungpati", "Gunungpati", 2, -7.0846, 110.3611, 900),
    ("Jl. Prof. Dr. Hamka", "Ngaliyan", 2, -6.9905, 110.3556, 800),
    ("Jl. Sekaran Raya", "Gunungpati", 2, -7.0560, 110.3924, 700),
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
            kecamatan TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            jam_buka TEXT NOT NULL,
            jam_tutup TEXT NOT NULL,
            status_aktif INTEGER NOT NULL DEFAULT 1
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
        "INSERT INTO spbu (nama, brand, alamat, kecamatan, latitude, longitude, jam_buka, jam_tutup) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
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
