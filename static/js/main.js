document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([-6.9932, 110.4203], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const spbuLayer = L.layerGroup().addTo(map);
    const zonaLayer = L.layerGroup();
    const rekomLayer = L.layerGroup();
    const accessLayer = L.layerGroup();
    const heatLayer = L.heatLayer([], {
        radius: 40,
        blur: 30,
        maxZoom: 15,
        gradient: {0.2: 'green', 0.5: 'yellow', 0.8: 'orange', 1.0: 'red'}
    });

    const spbuCount = document.getElementById('spbu-count');
    const zonaCount = document.getElementById('zona-count');
    const accessButton = document.getElementById('toggle-access');
    const loadingOverlay = document.getElementById('loading-overlay');
    const mapStatus = document.getElementById('map-status');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const brandFilter = document.getElementById('brand-filter');
    const kecamatanFilter = document.getElementById('kecamatan-filter');
    const resetFilters = document.getElementById('reset-filters');
    const exportButton = document.getElementById('export-button');

    let accessVisible = false;
    let spbuData = [];
    let zoneData = [];
    let spbuMarkers = [];

    const showLoading = () => {
        loadingOverlay.classList.remove('hidden');
        mapStatus.textContent = 'Memuat data peta...';
    };

    const hideLoading = () => {
        loadingOverlay.classList.add('hidden');
        mapStatus.textContent = 'Data peta siap ditampilkan';
    };

    const createBrandIcon = (color) => {
        return L.divIcon({
            className: 'custom-marker',
            html: `<div class="marker-icon ${color}"></div>`,
            iconSize: [24, 24],
            iconAnchor: [12, 12],
            popupAnchor: [0, -14]
        });
    };

    const brandIcons = {
        Pertamina: createBrandIcon('red'),
        Shell: createBrandIcon('yellow'),
        Vivo: createBrandIcon('blue'),
        default: createBrandIcon('blue')
    };

    const createRecommendationIcon = (rank) => {
        return L.divIcon({
            className: 'recommendation-marker',
            html: `<div>${rank}</div>`,
            iconSize: [38, 38],
            iconAnchor: [19, 19],
            popupAnchor: [0, -20]
        });
    };

    const createSPBUPopup = (item) => {
        return `
            <strong>${item.nama}</strong><br />
            <strong>Brand:</strong> ${item.brand}<br />
            <strong>Alamat:</strong> ${item.alamat}<br />
            <strong>Kecamatan:</strong> ${item.kecamatan}<br />
            <strong>Jam Operasional:</strong> ${item.jam_buka} - ${item.jam_tutup}
        `;
    };

    const getNearestKecamatan = (lat, lng) => {
        if (!zoneData.length) return 'Lainnya';
        const nearest = zoneData.reduce((best, zone) => {
            const distance = map.distance([lat, lng], [zone.latitude, zone.longitude]);
            if (!best || distance < best.distance) {
                return { distance, kecamatan: zone.kecamatan };
            }
            return best;
        }, null);
        return nearest ? nearest.kecamatan : 'Lainnya';
    };

    const setBrandOptions = () => {
        const uniqueKecamatans = new Set(zoneData.map((zone) => zone.kecamatan));
        const options = ['Semua', ...Array.from(uniqueKecamatans).sort()];
        kecamatanFilter.innerHTML = options.map((kec) => `<option value="${kec}">${kec}</option>`).join('');
    };

    const matchesFilters = (item) => {
        const brandValue = brandFilter.value;
        const kecamatanValue = kecamatanFilter.value;
        const query = searchInput.value.trim().toLowerCase();

        if (brandValue !== 'Semua' && item.brand !== brandValue) {
            return false;
        }
        if (kecamatanValue !== 'Semua' && item.kecamatan !== kecamatanValue) {
            return false;
        }
        if (query) {
            const text = `${item.nama} ${item.alamat}`.toLowerCase();
            return text.includes(query);
        }
        return true;
    };

    const refreshSPBU = () => {
        spbuLayer.clearLayers();
        const visibleItems = spbuMarkers.filter((entry) => matchesFilters(entry.item));
        visibleItems.forEach((entry) => spbuLayer.addLayer(entry.marker));
        mapStatus.textContent = `${visibleItems.length} SPBU sesuai filter`;
        return visibleItems;
    };

    const resetSearchAndFilters = () => {
        searchInput.value = '';
        brandFilter.value = 'Semua';
        kecamatanFilter.value = 'Semua';
        refreshSPBU();
    };

    const showMarkerBySearch = () => {
        const query = searchInput.value.trim().toLowerCase();
        const visibleItems = refreshSPBU();
        if (!query) return;
        const match = spbuMarkers.find((entry) => `${entry.item.nama} ${entry.item.alamat}`.toLowerCase().includes(query));
        if (match) {
            map.setView([match.item.latitude, match.item.longitude], 16);
            match.marker.openPopup();
            mapStatus.textContent = `Menampilkan hasil pencarian untuk "${searchInput.value.trim()}"`;
        } else {
            mapStatus.textContent = `Tidak ditemukan SPBU untuk "${searchInput.value.trim()}"`;
        }
    };

    const setSummaryCounts = () => {
        spbuCount.textContent = spbuData.length;
        zonaCount.textContent = zoneData.length;
    };

    const renderAccessAnalysis = (spbuData, blindSpotData) => {
        const bufferLayer = L.layerGroup();
        const blindLayer = L.layerGroup();

        spbuData.forEach((item) => {
            const buffer = L.circle([item.latitude, item.longitude], {
                radius: 2000,
                color: '#2563eb',
                fillColor: '#3b82f6',
                fillOpacity: 0.12,
                weight: 2,
                dashArray: '4 7'
            });
            bufferLayer.addLayer(buffer);
        });

        blindSpotData.forEach((item) => {
            const spot = L.circle([item.latitude, item.longitude], {
                radius: 330,
                color: '#f472b6',
                fillColor: '#fbcfe8',
                fillOpacity: 0.38,
                weight: 1
            }).bindPopup(`
                <strong>Blind Spot</strong><br />
                Area tanpa cakupan 2 km SPBU terdekat
            `);
            blindLayer.addLayer(spot);
        });

        accessLayer.clearLayers();
        accessLayer.addLayer(bufferLayer);
        accessLayer.addLayer(blindLayer);
    };

    const setAccessButtonState = () => {
        if (accessVisible) {
            accessButton.textContent = 'Sembunyikan Analisis Aksesibilitas';
            accessButton.classList.add('active');
        } else {
            accessButton.textContent = 'Tampilkan Analisis Aksesibilitas';
            accessButton.classList.remove('active');
        }
    };

    accessButton.addEventListener('click', () => {
        accessVisible = !accessVisible;
        if (accessVisible) {
            accessLayer.addTo(map);
        } else {
            map.removeLayer(accessLayer);
        }
        setAccessButtonState();
    });

    const initializeMarkers = () => {
        spbuMarkers = spbuData.map((item) => {
            const marker = L.marker([item.latitude, item.longitude], {
                icon: brandIcons[item.brand] || brandIcons.default
            });
            marker.bindPopup(createSPBUPopup(item));
            return { item, marker };
        });
        refreshSPBU();
    };

    const loadRecommendations = () => {
        fetch('/api/rekomendasi')
            .then((response) => response.json())
            .then((data) => {
                const recommendations = data.recommendations || [];
                recommendations.forEach((item) => {
                    const marker = L.marker([item.latitude, item.longitude], {
                        icon: createRecommendationIcon(item.rank)
                    }).bindPopup(`
                        <strong>Rekomendasi #${item.rank}</strong><br />
                        <strong>Skor Total:</strong> ${item.total_score}<br />
                        <strong>Kepadatan:</strong> ${item.density_score}<br />
                        <strong>Aksesibilitas:</strong> ${item.access_score}<br />
                        <strong>Jalan Utama:</strong> ${item.road_score}<br />
                        <strong>Alasan:</strong> ${item.reasons.join(', ')}
                    `);
                    rekomLayer.addLayer(marker);
                });
            })
            .catch((error) => {
                console.error('Gagal memuat rekomendasi lokasi:', error);
            });
    };

    const loadZoneData = () => {
        return fetch('/api/zona')
            .then((response) => response.json())
            .then((data) => {
                zoneData = data;
                setBrandOptions();
                zoneData.forEach((item) => {
                    const color = item.tingkat_kepadatan >= 4 ? '#dc2626' : item.tingkat_kepadatan === 3 ? '#f59e0b' : '#0284c7';
                    const circle = L.circle([item.latitude, item.longitude], {
                        radius: item.radius_meter,
                        color,
                        fillColor: color,
                        fillOpacity: 0.18,
                        weight: 2
                    }).bindPopup(`
                        <strong>${item.nama_zona}</strong><br />
                        Kecamatan: ${item.kecamatan}<br />
                        Kepadatan: ${item.tingkat_kepadatan}
                    `);
                    zonaLayer.addLayer(circle);
                    heatLayer.addLatLng([item.latitude, item.longitude, item.tingkat_kepadatan / 5]);
                });
                zonaCount.textContent = zoneData.length;
            });
    };

    const loadSPBUData = () => {
        return fetch('/api/spbu')
            .then((response) => response.json())
            .then((data) => {
                spbuData = data;
            });
    };

    const prepareSPBUData = () => {
        spbuData = spbuData.map((item) => ({
            ...item,
            kecamatan: getNearestKecamatan(item.latitude, item.longitude)
        }));
        initializeMarkers();
        setSummaryCounts();
    };

    const loadAccessAnalysis = () => {
        return fetch('/api/analisis-aksesibilitas')
            .then((response) => response.json())
            .then((analysis) => {
                renderAccessAnalysis(spbuData, analysis.blind_spots || []);
            });
    };

    const searchHandler = () => {
        showMarkerBySearch();
    };

    searchButton.addEventListener('click', (event) => {
        event.preventDefault();
        searchHandler();
    });

    searchInput.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            searchHandler();
        }
    });

    brandFilter.addEventListener('change', refreshSPBU);
    kecamatanFilter.addEventListener('change', refreshSPBU);
    resetFilters.addEventListener('click', () => {
        resetSearchAndFilters();
    });
    exportButton.addEventListener('click', () => {
        window.print();
    });

    const overlays = {
        'SPBU Eksisting': spbuLayer,
        'Kepadatan Lalu Lintas': zonaLayer,
        'Heatmap Kepadatan': heatLayer,
        'Rekomendasi Lokasi': rekomLayer
    };
    L.control.layers(null, overlays, { collapsed: false }).addTo(map);

    showLoading();
    Promise.all([loadZoneData(), loadSPBUData()])
        .then(() => {
            prepareSPBUData();
            loadRecommendations();
            return loadAccessAnalysis();
        })
        .then(() => {
            hideLoading();
        })
        .catch((error) => {
            hideLoading();
            mapStatus.textContent = 'Terjadi kesalahan saat memuat peta.';
            console.error('Gagal memuat data peta:', error);
        });
});
