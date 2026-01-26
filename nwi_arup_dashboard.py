"""
NWI Arup Geological Ground Model Dashboard
Flask application with Folium map showing Nederwiek I GGM (Arup) data

This is a backwards-compatible entry point. The code is organized in
the nwi_arup_dashboard package following separation of concerns:

- nwi_arup_dashboard/config.py       - Configuration constants
- nwi_arup_dashboard/data_loader.py  - GIS data loading logic
- nwi_arup_dashboard/map_builder.py  - Folium map construction
- nwi_arup_dashboard/routes.py       - Flask route handlers
- nwi_arup_dashboard/templates/      - HTML templates
- nwi_arup_dashboard/app.py          - Main entry point
"""

from nwi_arup_dashboard import create_app
from nwi_arup_dashboard.app import main

# Create app instance for backwards compatibility
app = create_app()

if __name__ == '__main__':
    main()
