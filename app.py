from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import sqlite3
import math

app = Flask(__name__)
CORS(app)

# SQLite database configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'spbu_semarang.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/spbu')
def api_spbu():
    conn = get_db_connection()
    cur = conn.execute('SELECT * FROM spbu')
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route('/api/zona')
def api_zona():
    conn = get_db_connection()
    cur = conn.execute('SELECT * FROM zona_lalu_lintas')
    rows = cur.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


def haversine_distance(lat1, lon1, lat2, lon2):
    r = 6371000  # radius bumi dalam meter
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


def compute_blind_spot_info(spbu_points):
    if not spbu_points:
        return {'blind_spots': [], 'grid_count': 0, 'blind_spot_count': 0, 'blind_spot_area': 0}

    min_lat, max_lat = -7.08, -6.90
    min_lng, max_lng = 110.30, 110.50
    step = 0.018

    cell_height = haversine_distance(min_lat, min_lng, min_lat + step, min_lng)
    cell_width = haversine_distance(min_lat, min_lng, min_lat, min_lng + step)
    cell_area_km2 = (cell_height * cell_width) / 1e6

    blind_spots = []
    grid_count = 0

    for lat in [min_lat + i * step for i in range(int((max_lat - min_lat) / step) + 1)]:
        for lng in [min_lng + j * step for j in range(int((max_lng - min_lng) / step) + 1)]:
            grid_count += 1
            covered = False
            for spbu_lat, spbu_lng in spbu_points:
                distance = haversine_distance(lat, lng, spbu_lat, spbu_lng)
                if distance <= 2000:
                    covered = True
                    break
            if not covered:
                blind_spots.append({'latitude': lat, 'longitude': lng})

    return {
        'blind_spots': blind_spots,
        'grid_count': grid_count,
        'blind_spot_count': len(blind_spots),
        'blind_spot_area': round(len(blind_spots) * cell_area_km2, 2)
    }


@app.route('/api/analisis-aksesibilitas')
def api_analisis_aksesibilitas():
    conn = get_db_connection()
    cur = conn.execute('SELECT latitude, longitude FROM spbu')
    spbu_rows = cur.fetchall()
    conn.close()

    spbu_points = [(row['latitude'], row['longitude']) for row in spbu_rows]
    return jsonify(compute_blind_spot_info(spbu_points))


@app.route('/api/rekomendasi')
def api_rekomendasi():
    conn = get_db_connection()
    spbu_rows = conn.execute('SELECT latitude, longitude FROM spbu').fetchall()
    zona_rows = conn.execute('SELECT latitude, longitude, tingkat_kepadatan, radius_meter FROM zona_lalu_lintas').fetchall()
    conn.close()

    spbu_points = [(row['latitude'], row['longitude']) for row in spbu_rows]
    zone_points = [
        {
            'latitude': row['latitude'],
            'longitude': row['longitude'],
            'density': row['tingkat_kepadatan'],
            'radius': row['radius_meter']
        }
        for row in zona_rows
    ]

    if not spbu_points or not zone_points:
        return jsonify({'recommendations': []})

    main_roads = [
        {'name': 'Jl. Pemuda', 'latitude': -6.9810, 'longitude': 110.4150},
        {'name': 'Jl. Pandanaran', 'latitude': -6.9735, 'longitude': 110.4190},
        {'name': 'Simpang Lima', 'latitude': -6.9815, 'longitude': 110.4105},
        {'name': 'Jl. Ahmad Yani', 'latitude': -6.9900, 'longitude': 110.4310},
        {'name': 'Jl. Gatot Subroto', 'latitude': -6.9860, 'longitude': 110.4345},
        {'name': 'Jl. Jend. Sudirman', 'latitude': -6.9930, 'longitude': 110.4250}
    ]

    min_lat, max_lat = -7.08, -6.90
    min_lng, max_lng = 110.30, 110.50
    step = 0.0045

    candidates = []

    for lat in [min_lat + i * step for i in range(int((max_lat - min_lat) / step) + 1)]:
        for lng in [min_lng + j * step for j in range(int((max_lng - min_lng) / step) + 1)]:
            candidates.append({'latitude': lat, 'longitude': lng})

    raw_scores = []
    max_density = 0
    max_access = 0
    max_road = 0

    for candidate in candidates:
        lat = candidate['latitude']
        lng = candidate['longitude']

        density_score = 0
        for zone in zone_points:
            dist = haversine_distance(lat, lng, zone['latitude'], zone['longitude'])
            influence = max(0, (zone['radius'] - dist) / zone['radius'])
            density_score += zone['density'] * influence

        nearest_spbu = min(haversine_distance(lat, lng, spbu_lat, spbu_lng) for spbu_lat, spbu_lng in spbu_points)
        access_score = min(nearest_spbu / 5000.0, 1.0) * 100

        nearest_road = min(haversine_distance(lat, lng, road['latitude'], road['longitude']) for road in main_roads)
        road_score = max(0.0, (3000.0 - nearest_road) / 3000.0) * 100

        raw_scores.append({
            'candidate': candidate,
            'density': density_score,
            'access': access_score,
            'road': road_score,
            'nearest_spbu': nearest_spbu,
            'nearest_road': nearest_road
        })

        max_density = max(max_density, density_score)
        max_access = max(max_access, access_score)
        max_road = max(max_road, road_score)

    if max_density == 0:
        max_density = 1
    if max_access == 0:
        max_access = 1
    if max_road == 0:
        max_road = 1

    for item in raw_scores:
        normalized_density = min(100, (item['density'] / max_density) * 100)
        normalized_access = min(100, item['access'])
        normalized_road = min(100, item['road'])
        total_score = normalized_density * 0.4 + normalized_access * 0.4 + normalized_road * 0.2

        reasons = []
        if normalized_density >= 65:
            reasons.append('Dekat zona kepadatan tinggi')
        if normalized_access >= 65:
            reasons.append('Terdekat dari SPBU eksisting relatif jauh')
        if normalized_road >= 65:
            reasons.append('Dekat jalan utama')
        if not reasons:
            reasons.append('Kombinasi keseimbangan kepadatan, akses, dan jalan utama')

        item.update({
            'normalized_density': round(normalized_density, 1),
            'normalized_access': round(normalized_access, 1),
            'normalized_road': round(normalized_road, 1),
            'total_score': round(total_score, 1),
            'reasons': reasons
        })

    recommendations = sorted(raw_scores, key=lambda x: x['total_score'], reverse=True)[:5]
    response = []

    for rank, item in enumerate(recommendations, start=1):
        response.append({
            'rank': rank,
            'latitude': item['candidate']['latitude'],
            'longitude': item['candidate']['longitude'],
            'total_score': item['total_score'],
            'density_score': item['normalized_density'],
            'access_score': item['normalized_access'],
            'road_score': item['normalized_road'],
            'reasons': item['reasons']
        })

    return jsonify({'recommendations': response})


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/tentang')
def tentang():
    return render_template('tentang.html')


@app.route('/api/statistik')
def api_statistik():
    conn = get_db_connection()
    spbu_rows = conn.execute('SELECT brand, latitude, longitude FROM spbu').fetchall()
    zona_rows = conn.execute('SELECT nama_zona, kecamatan, tingkat_kepadatan, latitude, longitude FROM zona_lalu_lintas').fetchall()
    conn.close()

    total_spbu = len(spbu_rows)
    brand_counts = {'Pertamina': 0, 'Shell': 0, 'Vivo': 0}
    for row in spbu_rows:
        brand = row['brand']
        if brand in brand_counts:
            brand_counts[brand] += 1
        else:
            brand_counts[brand] = brand_counts.get(brand, 0) + 1

    zone_items = [
        {
            'zone_name': row['nama_zona'],
            'kecamatan': row['kecamatan'],
            'density': row['tingkat_kepadatan'],
            'latitude': row['latitude'],
            'longitude': row['longitude']
        }
        for row in zona_rows
    ]

    kecamatan_counts = {}
    for spbu in spbu_rows:
        nearest_zone = min(
            zone_items,
            key=lambda zone: haversine_distance(spbu['latitude'], spbu['longitude'], zone['latitude'], zone['longitude'])
        )
        kecamatan = nearest_zone['kecamatan']
        kecamatan_counts[kecamatan] = kecamatan_counts.get(kecamatan, 0) + 1

    kecamatan_list = [
        {'kecamatan': kecamatan, 'count': count}
        for kecamatan, count in kecamatan_counts.items()
    ]
    kecamatan_list.sort(key=lambda x: x['count'], reverse=True)

    top_kecamatan = kecamatan_list[0]['kecamatan'] if kecamatan_list else '-'

    area_by_kecamatan = {
        'Semarang Tengah': 8.5,
        'Semarang Timur': 39.0,
        'Semarang Selatan': 47.5,
        'Semarang Utara': 33.0,
        'Pedurungan': 45.0,
        'Tanjung Mas': 11.2
    }

    kecamatan_table = []
    for item in kecamatan_list:
        kec = item['kecamatan']
        count = item['count']
        area = area_by_kecamatan.get(kec, 20.0)
        ratio = count / area if area > 0 else 0
        if ratio >= 0.35:
            status = 'Kritis'
        elif ratio >= 0.18:
            status = 'Kurang'
        else:
            status = 'Cukup'
        kecamatan_table.append({
            'kecamatan': kec,
            'count': count,
            'area_km2': area,
            'ratio': round(ratio, 3),
            'status': status
        })

    spbu_points = [(row['latitude'], row['longitude']) for row in spbu_rows]
    blind_spot_info = compute_blind_spot_info(spbu_points)
    blind_spot_area = blind_spot_info.get('blind_spot_area', 0)

    return jsonify({
        'total_spbu': total_spbu,
        'brand_counts': brand_counts,
        'kecamatan_counts': kecamatan_list,
        'kecamatan_with_most_spbu': top_kecamatan,
        'blind_spot_area': blind_spot_area,
        'zone_density': [
            {'zone_name': zone['zone_name'], 'density': zone['density']}
            for zone in zone_items
        ],
        'kecamatan_table': kecamatan_table
    })


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
