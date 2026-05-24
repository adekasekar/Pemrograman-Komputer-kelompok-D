document.addEventListener('DOMContentLoaded', function () {
    const totalSpbuEl = document.getElementById('total-spbu');
    const countPertaminaEl = document.getElementById('count-pertamina');
    const totalRekomendasiEl = document.getElementById('total-rekomendasi');
    const topKecamatanEl = document.getElementById('top-kecamatan');
    const blindspotAreaEl = document.getElementById('blindspot-area');
    const kecamatanTableBody = document.getElementById('kecamatan-table-body');

    Promise.all([
        fetch('/api/statistik').then((response) => response.json()),
        fetch('/api/rekomendasi').then((response) => response.json())
    ])
        .then(([statistikData, rekomendasiData]) => {
            // Tampilkan statistik SPBU
            totalSpbuEl.textContent = statistikData.total_spbu || 0;
            countPertaminaEl.textContent = statistikData.brand_counts.Pertamina || 0;
            topKecamatanEl.textContent = statistikData.kecamatan_with_most_spbu || '-';
            blindspotAreaEl.textContent = `${statistikData.blind_spot_area.toFixed(1)} km²`;

            // Tampilkan total rekomendasi
            const recommendations = rekomendasiData.recommendations || [];
            totalRekomendasiEl.textContent = recommendations.length;

            const kecamatanLabels = statistikData.kecamatan_counts.map((item) => item.kecamatan);
            const kecamatanValues = statistikData.kecamatan_counts.map((item) => item.count);
            const zoneLabels = statistikData.zone_density.map((item) => item.zone_name);
            const zoneValues = statistikData.zone_density.map((item) => item.density);

            new Chart(document.getElementById('spbuKecamatanChart'), {
                type: 'bar',
                data: {
                    labels: kecamatanLabels,
                    datasets: [{
                        label: 'Jumlah SPBU',
                        data: kecamatanValues,
                        backgroundColor: '#2563eb'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });

            new Chart(document.getElementById('kecamatanPieChart'), {
                type: 'pie',
                data: {
                    labels: kecamatanLabels,
                    datasets: [{
                        data: kecamatanValues,
                        backgroundColor: ['#dc2626', '#f97316', '#fb923c', '#f59e0b', '#34d399', '#60a5fa', '#818cf8', '#a855f7', '#ec4899', '#22c55e']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });

            new Chart(document.getElementById('zonaChart'), {
                type: 'bar',
                data: {
                    labels: zoneLabels,
                    datasets: [{
                        label: 'Tingkat Kepadatan',
                        data: zoneValues,
                        backgroundColor: '#f97316'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, max: 5 }
                    }
                }
            });

            // Chart untuk Top 10 Rekomendasi
            const topRekomendasi = recommendations.slice(0, 10);
            const rekomendasiLabels = topRekomendasi.map((item, idx) => `#${item.rank} ${item.location_name}`);
            const rekomendasiScores = topRekomendasi.map((item) => item.total_score);
            
            new Chart(document.getElementById('rekomendasiChart'), {
                type: 'bar',
                data: {
                    labels: rekomendasiLabels,
                    datasets: [{
                        label: 'Skor Total',
                        data: rekomendasiScores,
                        backgroundColor: '#C18DB4'
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { beginAtZero: true, max: 100 }
                    }
                }
            });

            statistikData.kecamatan_table.forEach((item) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${item.kecamatan}</td>
                    <td>${item.count}</td>
                    <td>${item.area_km2.toFixed(1)}</td>
                    <td>${item.ratio.toFixed(2)}</td>
                    <td><span class="status-chip ${item.status.toLowerCase()}">${item.status}</span></td>
                `;
                kecamatanTableBody.appendChild(row);
            });
        })
        .catch((error) => {
            console.error('Gagal memuat statistik:', error);
        });
});
