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
    'wind_farm': {
        'name': 'Wind Farm Zone',
        'gdb_layer': 'NW_Site_I_Wind_Farm_Zone',
        'show': True,
        'style': {'fillColor': 'green', 'color': 'darkgreen', 'weight': 3, 'fillOpacity': 0.1, 'dashArray': '10, 5'},
        'popup_fields': [],
    },
    'investigation_area': {
        'name': 'Investigation Area',
        'gdb_layer': 'NW_Site_I_Investigation_Area',
        'show': False,
        'style': {'fillColor': 'blue', 'color': 'blue', 'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'},
        'popup_fields': [],
    },
    'cables': {
        'name': 'Cables',
        'gdb_layer': 'Cables',
        'show': True,
        'style': {'color': 'orange', 'weight': 2, 'opacity': 0.8},
        'popup_fields': ['TYPE', 'OWNER', 'STATUS', 'NAME'],
    },
    'pipelines': {
        'name': 'Pipelines/Umbilicals',
        'gdb_layer': 'Pipelines_Umbilicals',
        'show': True,
        'style': {'color': 'red', 'weight': 2.5, 'opacity': 0.8},
        'popup_fields': ['NAME_FULL', 'MATERIAL', 'DIA_OUT_INCH', 'STATUS', 'OPERATOR'],
    },
    'infrastructure': {
        'name': 'As-found Infrastructure',
        'gdb_layer': 'Infrastructure_As_found_Infrastructure_Arc',
        'show': False,
        'style': {'color': 'brown', 'weight': 1.5, 'opacity': 0.7},
        'popup_fields': [],
    },
    'boreholes': {
        'name': 'Boreholes',
        'gdb_layer': 'Borehole_locations',
        'show': True,
        'point_style': {'radius': 6, 'color': 'darkblue', 'fillColor': 'blue', 'fillOpacity': 0.7},
        'popup_fields': ['Borehole_I', 'UWI'],
    },
    'pcpt': {
        'name': 'PCPT',
        'gdb_layer': 'PCPT',
        'show': False,
        'point_style': {'radius': 5, 'color': 'purple', 'fillColor': 'purple', 'fillOpacity': 0.6},
        'popup_fields': ['Location_ID'],
    },
    'vibrocore': {
        'name': 'VibroCore',
        'gdb_layer': 'VibroCore',
        'show': False,
        'point_style': {'radius': 5, 'color': 'green', 'fillColor': 'lightgreen', 'fillOpacity': 0.6},
        'popup_fields': ['Borehole_Sample__TestPoint'],
    },
}

# Dashboard statistics (can be updated dynamically)
DASHBOARD_STATS = {
    'cables': 47,
    'pipelines': 335,
    'boreholes': 68,
    'total_layers': 79,
}
