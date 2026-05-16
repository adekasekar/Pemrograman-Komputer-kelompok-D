document.addEventListener('DOMContentLoaded', function () {
    const totalSpbuEl = document.getElementById('total-spbu');
    const countPertaminaEl = document.getElementById('count-pertamina');
    const countShellEl = document.getElementById('count-shell');
    const countVivoEl = document.getElementById('count-vivo');
    const topKecamatanEl = document.getElementById('top-kecamatan');
    const blindspotAreaEl = document.getElementById('blindspot-area');
    const kecamatanTableBody = document.getElementById('kecamatan-table-body');

    fetch('/api/statistik')
        .then((response) => response.json())
        .then((data) => {
            totalSpbuEl.textContent = data.total_spbu || 0;
            countPertaminaEl.textContent = data.brand_counts.Pertamina || 0;
            countShellEl.textContent = data.brand_counts.Shell || 0;
            countVivoEl.textContent = data.brand_counts.Vivo || 0;
            topKecamatanEl.textContent = data.kecamatan_with_most_spbu || '-';
            blindspotAreaEl.textContent = `${data.blind_spot_area.toFixed(1)} km²`;

            const kecamatanLabels = data.kecamatan_counts.map((item) => item.kecamatan);
            const kecamatanValues = data.kecamatan_counts.map((item) => item.count);
            const zoneLabels = data.zone_density.map((item) => item.zone_name);
            const zoneValues = data.zone_density.map((item) => item.density);

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

            new Chart(document.getElementById('brandChart'), {
                type: 'pie',
                data: {
                    labels: ['Pertamina', 'Shell', 'Vivo'],
                    datasets: [{
                        data: [
                            data.brand_counts.Pertamina || 0,
                            data.brand_counts.Shell || 0,
                            data.brand_counts.Vivo || 0
                        ],
                        backgroundColor: ['#dc2626', '#f59e0b', '#0369a1']
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

            data.kecamatan_table.forEach((item) => {
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
