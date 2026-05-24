document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map', { zoomControl: false }).setView([-6.9932, 110.4203], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const spbuLayer = L.layerGroup();
    const zonaLayer = L.layerGroup();
    const rekomLayer = L.layerGroup();
    const accessLayer = L.layerGroup();

    const spbuCount = document.getElementById('spbu-count');
    const zonaCount = document.getElementById('zona-count');
    const accessButton = document.getElementById('toggle-access');
    const loadingOverlay = document.getElementById('loading-overlay');
    const mapStatus = document.getElementById('map-status');
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const brandFilter = document.getElementById('brand-filter');
    const kecamatanFilter = document.getElementById('kecamatan-filter');
    const kecamatanDropdownToggle = document.getElementById('kecamatan-dropdown-toggle');
    const kecamatanDropdown = document.getElementById('kecamatan-dropdown');
    const kecamatanSelected = document.getElementById('kecamatan-selected');
    const resetFilters = document.getElementById('reset-filters');

    const closeKecamatanDropdown = () => {
        if (kecamatanDropdown) kecamatanDropdown.classList.add('hidden');
        if (kecamatanDropdownToggle) kecamatanDropdownToggle.setAttribute('aria-expanded', 'false');
    };

    const openKecamatanDropdown = () => {
        if (kecamatanDropdown) kecamatanDropdown.classList.remove('hidden');
        if (kecamatanDropdownToggle) kecamatanDropdownToggle.setAttribute('aria-expanded', 'true');
    };

    // Ensure recommendation panel has no inline left positioning and enforce right/top
    const panelRekom = document.getElementById('panel-rekomendasi');
    if (panelRekom) {
        try {
            panelRekom.style.left = '';
            panelRekom.style.right = '8px';
            panelRekom.style.top = '10px';
            panelRekom.style.bottom = 'auto';
            panelRekom.style.maxHeight = 'calc(100vh - 220px)';
        } catch (e) { /* ignore */ }
    }

    let accessVisible = false;
    let spbuData = [];
    let zoneData = [];
    let spbuMarkers = [];
    let recommendationMarkers = [];

    const showLoading = () => {
        if (loadingOverlay) loadingOverlay.classList.remove('hidden');
        if (mapStatus) mapStatus.textContent = 'Memuat data peta...';
    };

    const hideLoading = () => {
        if (loadingOverlay) loadingOverlay.classList.add('hidden');
        if (mapStatus) mapStatus.textContent = 'Data peta siap ditampilkan';
    };

    const createBrandIcon = (color) => {
        return L.divIcon({
            className: 'custom-marker',
            html: '<div class="marker-icon ' + color + '"></div>',
            iconSize: [24, 24],
            iconAnchor: [12, 12],
            popupAnchor: [0, -14]
        });
    };

    const brandIcons = {
        Pertamina: createBrandIcon('red'),
        default: createBrandIcon('red')
    };

    const getRecommendationRankClass = (rank) => {
        if (rank <= 3) return 'gold';
        if (rank <= 6) return 'silver';
        return 'green';
    };

    const createRecommendationIcon = (rank) => {
        const rankClass = getRecommendationRankClass(rank);
        return L.divIcon({
            className: 'recommendation-marker ' + rankClass,
            html: '<div>' + rank + '</div>',
            iconSize: [42, 42],
            iconAnchor: [21, 21],
            popupAnchor: [0, -22]
        });
    };

const createRecommendationPopup = (item) => {
    const rankClass = item.rank <= 3 ? 'gold' : item.rank <= 6 ? 'silver' : 'green';
    const aksScore = Math.round(item.access_score);
    const denScore = Math.round(item.density_score);
    const roadScore = Math.round(item.road_score);
    return '<div class="panel-rank-badge">' +
        '<div class="panel-rank-number ' + rankClass + '">' + item.rank + '★</div>' +
        '<div class="panel-rank-info"><strong>#' + item.rank + ' Rekomendasi Terbaik</strong>' +
        '<span>' + item.location_name + '</span></div></div>' +
        '<div class="panel-total"><span class="panel-total-label">Skor Total</span>' +
        '<span class="panel-total-value">' + item.total_score + '/100</span></div>' +
        '<div class="panel-scores">' +
        '<div class="score-row"><span class="score-label">Aksesibilitas</span>' +
        '<div class="score-bar-wrap"><div class="score-bar aksesibilitas" style="width:' + aksScore + '%"></div></div>' +
        '<span class="score-value">' + aksScore + '</span></div>' +
        '<div class="score-row"><span class="score-label">Kepadatan</span>' +
        '<div class="score-bar-wrap"><div class="score-bar kepadatan" style="width:' + denScore + '%"></div></div>' +
        '<span class="score-value">' + denScore + '</span></div>' +
        '<div class="score-row"><span class="score-label">Jalan Utama</span>' +
        '<div class="score-bar-wrap"><div class="score-bar jalan" style="width:' + roadScore + '%"></div></div>' +
        '<span class="score-value">' + roadScore + '</span></div></div>' +
        '<div class="panel-details">' +
        '<div class="detail-row"><span class="detail-icon">📍</span><span class="detail-text"><strong>SPBU Terdekat:</strong> ' + item.nearest_spbu_name + '</span></div>' +
        '<div class="detail-row"><span class="detail-icon">📏</span><span class="detail-text"><strong>Jarak:</strong> ' + item.nearest_spbu_distance_km + ' km</span></div>' +
        '<div class="detail-row"><span class="detail-icon">🚦</span><span class="detail-text">' + item.density_explanation + '</span></div></div>' +
        '<div class="panel-alasan"><div class="panel-alasan-title">💡 Alasan Rekomendasi</div>' +
        '<div class="panel-alasan-text">' + item.reasons + '</div></div>';
};

    const createSPBUPopup = (item) => {
        return '<strong>' + item.nama + '</strong><br />' +
            '<strong>Brand:</strong> ' + item.brand + '<br />' +
            '<strong>Alamat:</strong> ' + item.alamat + '<br />' +
            '<strong>Kecamatan:</strong> ' + item.kecamatan + '<br />' +
            '<strong>Jam Operasional:</strong> ' + item.jam_buka + ' - ' + item.jam_tutup;
    };

    const setKecamatanOptions = () => {
        if (!kecamatanFilter || !kecamatanDropdown || !kecamatanSelected) return;
        const uniqueKecamatans = new Set(
            spbuData
                .map(function(item) { return item.kecamatan; })
                .filter(function(kec) { return kec && kec.trim() !== '' && kec !== 'Lainnya'; })
        );
        const sorted = Array.from(uniqueKecamatans).sort(function(a, b) {
            return a.localeCompare(b, 'id');
        });
        const options = ['Semua'].concat(sorted);
        kecamatanDropdown.innerHTML = options.map(function(kec) {
            return '<button type="button" class="kecamatan-option' + (kec === 'Semua' ? ' active' : '') + '" data-value="' + kec + '">' + kec + '</button>';
        }).join('');
        kecamatanFilter.value = 'Semua';
        kecamatanSelected.textContent = 'Semua';
    };

    const matchesFilters = (item) => {
        const brandValue = brandFilter ? brandFilter.value : 'Semua';
        const kecamatanValue = kecamatanFilter ? kecamatanFilter.value : 'Semua';
        const query = searchInput ? searchInput.value.trim().toLowerCase() : '';

        if (brandValue !== 'Semua' && item.brand !== brandValue) {
            return false;
        }
        if (kecamatanValue !== 'Semua' && item.kecamatan !== kecamatanValue) {
            return false;
        }
        if (query) {
            const text = (item.nama + ' ' + item.alamat).toLowerCase();
            return text.includes(query);
        }
        return true;
    };

    const refreshSPBU = () => {
        spbuLayer.clearLayers();
        if (!map.hasLayer(spbuLayer)) spbuLayer.addTo(map);
        const visibleItems = spbuMarkers.filter(function(entry) {
            return matchesFilters(entry.item);
        });
        visibleItems.forEach(function(entry) {
            spbuLayer.addLayer(entry.marker);
        });
        if (mapStatus) mapStatus.textContent = visibleItems.length + ' SPBU sesuai filter';
        return visibleItems;
    };

    const resetSearchAndFilters = () => {
        if (searchInput) searchInput.value = '';
        if (brandFilter) brandFilter.value = 'Semua';
        if (kecamatanFilter) kecamatanFilter.value = 'Semua';
        refreshSPBU();
    };

    const showMarkerBySearch = () => {
        const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
        refreshSPBU();
        if (!query) return;
        const match = spbuMarkers.find(function(entry) {
            return (entry.item.nama + ' ' + entry.item.alamat).toLowerCase().includes(query);
        });
        if (match) {
            map.setView([match.item.latitude, match.item.longitude], 16);
            match.marker.openPopup();
            if (mapStatus) mapStatus.textContent = 'Menampilkan hasil pencarian untuk "' + searchInput.value.trim() + '"';
        } else {
            if (mapStatus) mapStatus.textContent = 'Tidak ditemukan SPBU untuk "' + (searchInput ? searchInput.value.trim() : '') + '"';
        }
    };

    const setSummaryCounts = () => {
        if (spbuCount) spbuCount.textContent = spbuData.length;
        if (zonaCount) zonaCount.textContent = zoneData.length;
    };

    const renderAccessAnalysis = (spbuDataParam, blindSpotData) => {
        const bufferLayer = L.layerGroup();
        const blindLayer = L.layerGroup();

        spbuDataParam.forEach(function(item) {
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

        blindSpotData.forEach(function(item) {
            const spot = L.circle([item.latitude, item.longitude], {
                radius: 330,
                color: '#f472b6',
                fillColor: '#fbcfe8',
                fillOpacity: 0.38,
                weight: 1
            }).bindPopup('<strong>Blind Spot</strong><br />Area tanpa cakupan 2 km SPBU terdekat');
            blindLayer.addLayer(spot);
        });

        accessLayer.clearLayers();
        accessLayer.addLayer(bufferLayer);
        accessLayer.addLayer(blindLayer);
    };

    const setAccessButtonState = () => {
        if (!accessButton) return;
        if (accessVisible) {
            accessButton.textContent = 'Sembunyikan Analisis Aksesibilitas';
            accessButton.classList.add('active');
        } else {
            accessButton.textContent = 'Tampilkan Analisis Aksesibilitas';
            accessButton.classList.remove('active');
        }
    };

    if (accessButton) {
        accessButton.addEventListener('click', function() {
            accessVisible = !accessVisible;
            if (accessVisible) {
                accessLayer.addTo(map);
            } else {
                map.removeLayer(accessLayer);
            }
            setAccessButtonState();
        });
    }

    const initializeMarkers = () => {
        spbuMarkers = spbuData.map(function(item) {
            const marker = L.marker([item.latitude, item.longitude], {
                icon: brandIcons[item.brand] || brandIcons.default
            });
            marker.bindPopup(createSPBUPopup(item));
            return { item: item, marker: marker };
        });
        refreshSPBU();
    };

    const loadRecommendations = () => {
        return fetch('/api/rekomendasi')
            .then(function(response) { return response.json(); })
            .then(function(data) {
                const recommendations = data.recommendations || [];
                rekomLayer.clearLayers();
                recommendationMarkers = recommendations.map(function(item) {
                    const marker = L.marker([item.latitude, item.longitude], {
icon: createRecommendationIcon(item.rank)
                    });
                    marker.on('click', function() {
                        const panel = document.getElementById('panel-rekomendasi');
                        const content = document.getElementById('panel-content');
                        if (panel && content) {
                            content.innerHTML = createRecommendationPopup(item);
                            panel.classList.remove('hidden');
                        }
                    });
                    rekomLayer.addLayer(marker);
                    return { rank: item.rank, item: item, marker: marker };
                });
            })
            .catch(function(error) {
                console.error('Gagal memuat rekomendasi lokasi:', error);
            });
    };

    const loadZoneData = () => {
        return fetch('/api/zona')
            .then(function(response) { return response.json(); })
            .then(function(data) {
                zoneData = data;
                zoneData.forEach(function(item) {
                    const color = item.tingkat_kepadatan >= 4 ? '#dc2626' : item.tingkat_kepadatan === 3 ? '#f59e0b' : '#0284c7';
                    const circle = L.circle([item.latitude, item.longitude], {
                        radius: item.radius_meter,
                        color: color,
                        fillColor: color,
                        fillOpacity: 0.18,
                        weight: 2
                    }).bindPopup('<strong>' + item.nama_zona + '</strong><br />Kecamatan: ' + item.kecamatan + '<br />Kepadatan: ' + item.tingkat_kepadatan);
                    zonaLayer.addLayer(circle);
                });
                if (zonaCount) zonaCount.textContent = zoneData.length;
            });
    };

    const loadSPBUData = () => {
        return fetch('/api/spbu')
            .then(function(response) { return response.json(); })
            .then(function(data) {
                spbuData = data;
            });
    };

    const prepareSPBUData = () => {
        setKecamatanOptions();
        initializeMarkers();
        setSummaryCounts();
    };

    const loadAccessAnalysis = () => {
        return fetch('/api/analisis-aksesibilitas')
            .then(function(response) { return response.json(); })
            .then(function(analysis) {
                renderAccessAnalysis(spbuData, analysis.blind_spots || []);
            });
    };

    if (searchButton) {
        searchButton.addEventListener('click', function(event) {
            event.preventDefault();
            showMarkerBySearch();
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                showMarkerBySearch();
            }
        });
    }

    if (brandFilter) brandFilter.addEventListener('change', refreshSPBU);
    if (resetFilters) resetFilters.addEventListener('click', function() {
        resetSearchAndFilters();
        closeKecamatanDropdown();
    });

    if (kecamatanDropdownToggle) {
        kecamatanDropdownToggle.addEventListener('click', function(event) {
            event.stopPropagation();
            if (!kecamatanDropdown) return;
            if (kecamatanDropdown.classList.contains('hidden')) {
                openKecamatanDropdown();
            } else {
                closeKecamatanDropdown();
            }
        });
    }

    if (kecamatanDropdown) {
        kecamatanDropdown.addEventListener('click', function(event) {
            const target = event.target;
            if (!target.classList.contains('kecamatan-option')) return;
            const value = target.dataset.value;
            if (!value) return;
            if (kecamatanFilter) kecamatanFilter.value = value;
            if (kecamatanSelected) kecamatanSelected.textContent = value;
            Array.from(kecamatanDropdown.querySelectorAll('.kecamatan-option')).forEach(function(item) {
                item.classList.toggle('active', item.dataset.value === value);
            });
            refreshSPBU();
            closeKecamatanDropdown();
        });
    }

    document.addEventListener('click', function(event) {
        if (!kecamatanDropdown || !kecamatanDropdownToggle) return;
        const target = event.target;
        if (!kecamatanDropdown.contains(target) && !kecamatanDropdownToggle.contains(target)) {
            closeKecamatanDropdown();
        }
    });

    const overlays = {
        'SPBU Eksisting': spbuLayer,
        'Kepadatan Lalu Lintas': zonaLayer,
        'Analisis Aksesibilitas': accessLayer,
        'Rekomendasi Lokasi': rekomLayer
    };

    // Setup custom layer control bindings to the checkboxes in DOM
    const setupLayerControl = () => {
        const chkSpbu = document.getElementById('chk-spbu');
        const chkZona = document.getElementById('chk-zona');
        const chkAccess = document.getElementById('chk-access');
        const chkRekom = document.getElementById('chk-rekom');

        if (chkSpbu) {
            chkSpbu.checked = true;
            chkSpbu.addEventListener('change', function(e) {
                if (e.target.checked) map.addLayer(spbuLayer);
                else map.removeLayer(spbuLayer);
            });
        }
        if (chkZona) {
            chkZona.addEventListener('change', function(e) {
                if (e.target.checked) map.addLayer(zonaLayer);
                else map.removeLayer(zonaLayer);
            });
        }
        if (chkAccess) {
            chkAccess.addEventListener('change', function(e) {
                accessVisible = !!e.target.checked;
                if (accessVisible) map.addLayer(accessLayer);
                else map.removeLayer(accessLayer);
                setAccessButtonState();
            });
        }
        if (chkRekom) {
            chkRekom.addEventListener('change', function(e) {
                if (e.target.checked) map.addLayer(rekomLayer);
                else map.removeLayer(rekomLayer);
            });
        }
        // apply initial checkbox states to map
        try {
            if (chkSpbu && chkSpbu.checked) map.addLayer(spbuLayer);
            if (chkZona && chkZona.checked) map.addLayer(zonaLayer);
            if (chkAccess && chkAccess.checked) { accessVisible = true; map.addLayer(accessLayer); }
            if (chkRekom && chkRekom.checked) map.addLayer(rekomLayer);
        } catch (e) { /* ignore */ }
    };

    // Add zoom control at bottom-left explicitly
    L.control.zoom({ position: 'bottomleft' }).addTo(map);

    const applyUrlParams = () => {
        const urlParams = new URLSearchParams(window.location.search);
        const layer = urlParams.get('layer');
        const focus = urlParams.get('focus');

        if (layer === 'spbu') {
            if (!map.hasLayer(spbuLayer)) map.addLayer(spbuLayer);
        }
        if (layer === 'kepadatan') {
            if (!map.hasLayer(zonaLayer)) map.addLayer(zonaLayer);
        }
        if (layer === 'rekomendasi') {
            if (!map.hasLayer(rekomLayer)) map.addLayer(rekomLayer);
        }
        if (layer === 'aksesibilitas') {
            accessVisible = true;
            if (!map.hasLayer(accessLayer)) map.addLayer(accessLayer);
            setAccessButtonState();
        }
        if (focus === 'search' && searchInput) {
            searchInput.focus();
        }
    };
const closePanel = document.getElementById('close-panel');
if (closePanel) {
    closePanel.addEventListener('click', function() {
        document.getElementById('panel-rekomendasi').classList.add('hidden');
    });
}
    showLoading();

    Promise.all([loadZoneData(), loadSPBUData()])
        .then(function() {
            prepareSPBUData();
            return Promise.all([loadRecommendations(), loadAccessAnalysis()]);
        })
        .then(function() {
            // initialize custom layer control after layers and markers loaded
            try { setupLayerControl(); } catch (e) { console.warn('Layer control init failed', e); }
            applyUrlParams();
            hideLoading();
        })
        .catch(function(error) {
            hideLoading();
            if (mapStatus) mapStatus.textContent = 'Terjadi kesalahan saat memuat peta.';
            console.error('Gagal memuat data peta:', error);
        });
});