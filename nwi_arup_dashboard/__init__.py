"""
NWI Arup Dashboard Package
Flask application with Folium map showing Nederwiek I Geological Ground Model (Arup) data
"""

from flask import Flask


def create_app():
    """Application factory for creating the Flask app."""
    application = Flask(__name__, template_folder='templates')

    from .routes import register_routes
    register_routes(application)

    # Preload GIS data at startup
    from .map_builder import get_layers
    with application.app_context():
        get_layers()

    return application


# Create app instance for gunicorn
app = create_app()
