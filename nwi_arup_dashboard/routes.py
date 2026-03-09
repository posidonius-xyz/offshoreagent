"""
Flask route handlers for the NWI Arup Dashboard
"""

from flask import render_template, jsonify, Response

from .config import DASHBOARD_STATS, LAYER_CONFIGS, DEFAULT_CENTER_LAT, DEFAULT_CENTER_LON, DEFAULT_ZOOM
from .data_loader import load_single_layer


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
        return render_template('map.html',
                               center_lat=DEFAULT_CENTER_LAT,
                               center_lon=DEFAULT_CENTER_LON,
                               zoom=DEFAULT_ZOOM)

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
