"""
Flask route handlers for the NWI Arup Dashboard
"""

import json
from flask import render_template, jsonify, Response

from .config import DASHBOARD_STATS, LAYER_CONFIGS, DEFAULT_CENTER_LAT, DEFAULT_CENTER_LON, DEFAULT_ZOOM
from .data_loader import load_single_layer


MAP_HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
html, body, #map { margin: 0; padding: 0; width: 100%%; height: 100%%; }
#loading {
    position: absolute; top: 10px; right: 10px; z-index: 1000;
    background: rgba(255,255,255,0.95); padding: 8px 14px; border-radius: 6px;
    font: 13px/1.4 system-ui, sans-serif; box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    max-width: 220px;
}
#loading .bar { height: 3px; background: #e0e0e0; border-radius: 2px; margin-top: 6px; }
#loading .bar-fill { height: 100%%; background: #1a73e8; border-radius: 2px; transition: width 0.3s; width: 0%%; }
#loading.done { display: none; }
</style>
</head>
<body>
<div id="map"></div>
<div id="loading">
    <div id="loading-text">Loading layers...</div>
    <div class="bar"><div class="bar-fill" id="loading-bar"></div></div>
</div>
<script>
(function() {
    var map = L.map('map').setView([%(center_lat)s, %(center_lon)s], %(zoom)s);

    var baseLayers = {
        'OpenStreetMap': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: 'OpenStreetMap'}).addTo(map),
        'Satellite': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {attribution: 'Esri'}),
        'Ocean': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}', {attribution: 'Esri'})
    };

    var overlays = {};
    var layerControl = L.control.layers(baseLayers, overlays, {collapsed: false}).addTo(map);

    function buildPopup(props, fields) {
        if (!fields || fields.length === 0) return null;
        var html = '<div style="font:13px system-ui,sans-serif">';
        fields.forEach(function(f) {
            var val = props[f];
            if (val !== undefined && val !== null && val !== 'None' && val !== 'nan') {
                html += '<b>' + f + ':</b> ' + val + '<br>';
            }
        });
        return html + '</div>';
    }

    function addLayerToMap(key, geojson, config) {
        var layer;
        if (config.point_style) {
            var ps = config.point_style;
            layer = L.geoJSON(geojson, {
                pointToLayer: function(feature, latlng) {
                    return L.circleMarker(latlng, {
                        radius: ps.radius || 5,
                        color: ps.color || 'blue',
                        fillColor: ps.fillColor || ps.color || 'blue',
                        fillOpacity: ps.fillOpacity || 0.6,
                        weight: ps.weight || 1
                    });
                },
                onEachFeature: function(feature, layer) {
                    var popup = buildPopup(feature.properties, config.popup_fields);
                    if (popup) layer.bindPopup(popup, {maxWidth: 300});
                }
            });
        } else {
            var style = config.style || {color: 'blue', weight: 2};
            layer = L.geoJSON(geojson, {
                style: function() { return style; },
                onEachFeature: function(feature, layer) {
                    var popup = buildPopup(feature.properties, config.popup_fields);
                    if (popup) layer.bindPopup(popup, {maxWidth: 300});
                }
            });
        }

        var name = config.name + ' (' + geojson.features.length + ')';
        overlays[name] = layer;
        if (config.show) layer.addTo(map);
        layerControl.addOverlay(layer, name);
    }

    async function loadLayers() {
        var el = document.getElementById('loading-text');
        var bar = document.getElementById('loading-bar');
        var loading = document.getElementById('loading');

        try {
            var res = await fetch('api/layers');
            var layers = await res.json();
            var total = layers.length;

            for (var i = 0; i < total; i++) {
                var cfg = layers[i];
                el.textContent = 'Loading ' + cfg.name + '... (' + (i+1) + '/' + total + ')';
                bar.style.width = ((i+1) / total * 100) + '%%';
                try {
                    var r = await fetch('api/layer/' + cfg.key);
                    if (r.ok) {
                        var geojson = await r.json();
                        if (geojson.features && geojson.features.length > 0) {
                            addLayerToMap(cfg.key, geojson, cfg);
                        }
                    }
                } catch(e) { console.warn('Failed to load layer:', cfg.key, e); }
            }
        } catch(e) { console.error('Failed to fetch layer list:', e); }

        loading.className = 'done';
    }

    loadLayers();
})();
</script>
</body>
</html>"""


def register_routes(app):
    """Register all routes with the Flask app."""

    @app.route('/')
    def index():
        """Main dashboard route with header and embedded map."""
        map_html = '<iframe src="map" style="width:100%; height:100%; border:none;"></iframe>'
        return render_template('dashboard.html', map_html=map_html, stats=DASHBOARD_STATS)

    @app.route('/map')
    def map_view():
        """Return Leaflet map that loads layers progressively."""
        return MAP_HTML % {
            'center_lat': DEFAULT_CENTER_LAT,
            'center_lon': DEFAULT_CENTER_LON,
            'zoom': DEFAULT_ZOOM,
        }

    @app.route('/fullscreen')
    def fullscreen():
        """Full screen map only view."""
        from .map_builder import create_map
        m = create_map()
        return m._repr_html_()

    @app.route('/api/layers')
    def api_layers():
        """Return list of available layers with their configs."""
        layers = []
        for key, config in LAYER_CONFIGS.items():
            layers.append({
                'key': key,
                'name': config['name'],
                'show': config.get('show', False),
                'style': config.get('style'),
                'point_style': config.get('point_style'),
                'popup_fields': config.get('popup_fields', []),
            })
        return jsonify(layers)

    @app.route('/api/layer/<key>')
    def api_layer(key):
        """Return GeoJSON for a single layer."""
        gdf = load_single_layer(key)
        if gdf is None or len(gdf) == 0:
            return jsonify({'type': 'FeatureCollection', 'features': []})
        return Response(gdf.to_json(), mimetype='application/json')
