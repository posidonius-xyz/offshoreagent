"""
Flask route handlers for the Infrastructure Dashboard
"""

from flask import render_template

from .config import DASHBOARD_STATS
from .map_builder import create_map


def register_routes(app):
    """Register all routes with the Flask app."""

    @app.route('/')
    def index():
        """Main dashboard route with header and embedded map."""
        map_html = '<iframe src="/map" style="width:100%; height:100%; border:none;"></iframe>'
        return render_template('dashboard.html', map_html=map_html, stats=DASHBOARD_STATS)

    @app.route('/map')
    def map_view():
        """Return just the Folium map for iframe embedding."""
        m = create_map()
        return m.get_root().render()

    @app.route('/fullscreen')
    def fullscreen():
        """Full screen map only view."""
        m = create_map()
        return m._repr_html_()
