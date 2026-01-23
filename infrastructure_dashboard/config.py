"""
Configuration constants for the Infrastructure Dashboard
"""

import os

# GDB file path (relative to project root)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDB_PATH = os.path.join(_PROJECT_ROOT, "data-extracted", "RVO_NW_I_GGM.gdb")

# Default map center (North Sea)
DEFAULT_CENTER_LAT = 52.5
DEFAULT_CENTER_LON = 4.0
DEFAULT_ZOOM = 10

# Layer configurations
LAYER_CONFIGS = {
    'cables': {
        'name': 'Cables',
        'gdb_layer': 'Cables',
        'show': True,
    },
    'pipelines': {
        'name': 'Pipelines_Umbilicals',
        'gdb_layer': 'Pipelines_Umbilicals',
        'show': True,
    },
    'infrastructure': {
        'name': 'Infrastructure_As_found_Infrastructure_Arc',
        'gdb_layer': 'Infrastructure_As_found_Infrastructure_Arc',
        'show': False,
    },
    'wind_farm': {
        'name': 'NW_Site_I_Wind_Farm_Zone',
        'gdb_layer': 'NW_Site_I_Wind_Farm_Zone',
        'show': True,
    },
    'investigation_area': {
        'name': 'NW_Site_I_Investigation_Area',
        'gdb_layer': 'NW_Site_I_Investigation_Area',
        'show': False,
    },
    'boreholes': {
        'name': 'Borehole_locations',
        'gdb_layer': 'Borehole_locations',
        'show': True,
    },
    'pcpt': {
        'name': 'PCPT',
        'gdb_layer': 'PCPT',
        'show': False,
    },
    'vibrocore': {
        'name': 'VibroCore',
        'gdb_layer': 'VibroCore',
        'show': False,
    },
}

# Dashboard statistics (can be updated dynamically)
DASHBOARD_STATS = {
    'cables': 47,
    'pipelines': 335,
    'boreholes': 68,
    'total_layers': 79,
}
