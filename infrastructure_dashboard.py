"""
Interactive Infrastructure Dashboard
Flask application with Folium map showing infrastructure assets from Nederwiek I GDB

This is a backwards-compatible entry point. The code has been reorganized into
the infrastructure_dashboard package following separation of concerns:

- infrastructure_dashboard/config.py       - Configuration constants
- infrastructure_dashboard/data_loader.py  - GIS data loading logic
- infrastructure_dashboard/map_builder.py  - Folium map construction
- infrastructure_dashboard/routes.py       - Flask route handlers
- infrastructure_dashboard/templates/      - HTML templates
- infrastructure_dashboard/app.py          - Main entry point
"""

from infrastructure_dashboard import create_app
from infrastructure_dashboard.app import main

# Create app instance for backwards compatibility
app = create_app()

if __name__ == '__main__':
    main()
