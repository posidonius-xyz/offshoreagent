"""
Configuration constants for the TNW Infrastructure Dashboard
"""

import os

# GDB file path (relative to project root)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDB_PATH = os.path.join(_PROJECT_ROOT, "data-extracted", "TNW_GP", "10_GDB", "103270_RVO_TNW_GIS_Database_MMT.gdb")

# Default map center (TNW offshore area, North Sea)
DEFAULT_CENTER_LAT = 52.75
DEFAULT_CENTER_LON = 4.35
DEFAULT_ZOOM = 10

# Layer configurations
LAYER_CONFIGS = {
    # Wind Farm Zones
    'wind_farms': {
        'name': 'Wind Farm Zones',
        'gdb_layer': 'DNZ_windparken',
        'show': True,
        'style': {'fillColor': 'green', 'color': 'darkgreen', 'weight': 3, 'fillOpacity': 0.15, 'dashArray': '10, 5'},
        'popup_fields': ['NAAM', 'NAME', 'EIGENAAR', 'STATUS'],
    },
    'designated_wind_areas': {
        'name': 'Designated Wind Areas',
        'gdb_layer': 'ZDv_aangewez_windgebied_nwp',
        'show': False,
        'style': {'fillColor': 'lightgreen', 'color': 'green', 'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'},
        'popup_fields': [],
    },
    'wind_farm_buffer': {
        'name': 'Wind Farm Buffer',
        'gdb_layer': 'windparken_buffer',
        'show': False,
        'style': {'fillColor': 'green', 'color': 'green', 'weight': 1, 'fillOpacity': 0.05, 'dashArray': '3, 3'},
        'popup_fields': [],
    },
    'turbines': {
        'name': 'Wind Turbines',
        'gdb_layer': 'windparken_turbines',
        'show': True,
        'point_style': {'radius': 4, 'color': 'darkgreen', 'fillColor': '#00cc00', 'fillOpacity': 0.8},
        'popup_fields': ['NAAM', 'STATUS'],
    },
    # Infrastructure
    'cables': {
        'name': 'Cables',
        'gdb_layer': 'ZDl_electra_telecom_kabels',
        'show': True,
        'style': {'color': 'orange', 'weight': 3, 'opacity': 0.8},
        'popup_fields': ['NAAM', 'NAME', 'KABEL_TYPE', 'TYPE', 'EIGENAAR', 'OWNER'],
    },
    'cables_buffer': {
        'name': 'Cables Buffer',
        'gdb_layer': 'ZDl_electra_telecom_kabels_buffer',
        'show': False,
        'style': {'fillColor': 'orange', 'color': 'orange', 'weight': 1, 'fillOpacity': 0.05},
        'popup_fields': [],
    },
    'pipelines': {
        'name': 'Pipelines',
        'gdb_layer': 'ZDl_leidingen',
        'show': True,
        'style': {'color': 'red', 'weight': 3, 'opacity': 0.8},
        'popup_fields': ['LEID_NR', 'TYPE', 'OPERATOR', 'STATUS'],
    },
    'pipelines_buffer': {
        'name': 'Pipelines Buffer',
        'gdb_layer': 'WOZ_leidingen_buffer_20160217',
        'show': False,
        'style': {'fillColor': 'red', 'color': 'red', 'weight': 1, 'fillOpacity': 0.05},
        'popup_fields': [],
    },
    # Survey Areas
    'survey_boundary': {
        'name': 'Survey Boundary',
        'gdb_layer': 'MMT_270_Survey_Boundary',
        'show': True,
        'style': {'fillColor': 'lightblue', 'color': 'blue', 'weight': 2, 'fillOpacity': 0.1, 'dashArray': '5, 5'},
        'popup_fields': ['SURVEY_ID', 'COMMENT'],
    },
    'project_area': {
        'name': 'Project Area',
        'gdb_layer': 'MMT_270_Project_Area',
        'show': False,
        'style': {'fillColor': 'lightyellow', 'color': 'goldenrod', 'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'},
        'popup_fields': [],
    },
    # Hazards & Geological Features
    'hazards_polygon': {
        'name': 'Hazards (Areas)',
        'gdb_layer': 'MMT_270_RVO_HAZARDS_PGN',
        'show': True,
        'style': {'fillColor': '#ffcccc', 'color': 'red', 'weight': 2, 'fillOpacity': 0.4},
        'popup_fields': ['HAZARD', 'LAYER', 'COMMENT'],
    },
    'hazards_line': {
        'name': 'Hazards (Linear)',
        'gdb_layer': 'MMT_270_RVO_HAZARDS_LIN',
        'show': False,
        'style': {'color': 'red', 'weight': 2, 'opacity': 0.8},
        'popup_fields': ['HAZARD', 'COMMENT'],
    },
    'hazards_point': {
        'name': 'Hazards (Points)',
        'gdb_layer': 'MMT_270_RVO_HAZARDS_PNT',
        'show': False,
        'point_style': {'radius': 5, 'color': 'red', 'fillColor': '#ff6666', 'fillOpacity': 0.7},
        'popup_fields': ['HAZARD', 'COMMENT'],
    },
    'faults': {
        'name': 'Faults',
        'gdb_layer': 'MMT_270_RVO_FAULTS_LIN',
        'show': True,
        'style': {'color': 'brown', 'weight': 3, 'opacity': 0.9, 'dashArray': '5, 3'},
        'popup_fields': ['HAZARD', 'COMMENT'],
    },
    'bedforms': {
        'name': 'Bedforms',
        'gdb_layer': 'MMT_270_RVO_Bedforms_PGN',
        'show': False,
        'style': {'fillColor': '#DAA520', 'color': '#B8860B', 'weight': 1, 'fillOpacity': 0.3},
        'popup_fields': [],
    },
    'sediments': {
        'name': 'Sediments',
        'gdb_layer': 'RVO_MMT_103270_Sediments_PGN',
        'show': False,
        'style': {'fillColor': '#DAA520', 'color': '#B8860B', 'weight': 1, 'fillOpacity': 0.3},
        'popup_fields': [],
    },
    # Survey Data
    'known_objects': {
        'name': 'Known Objects',
        'gdb_layer': 'TNW_Known_Objects',
        'show': True,
        'point_style': {'radius': 7, 'color': 'darkviolet', 'fillColor': 'purple', 'fillOpacity': 0.7},
        'popup_fields': ['NCN', 'DHY'],
    },
    'grab_samples': {
        'name': 'Grab Samples',
        'gdb_layer': 'MMT_270_RVO_Grab_Sample_Listing',
        'show': False,
        'point_style': {'radius': 5, 'color': 'darkorange', 'fillColor': 'orange', 'fillOpacity': 0.7},
        'popup_fields': ['ID', 'DESCRIPTION'],
    },
    'sss_contacts': {
        'name': 'SSS Contacts',
        'gdb_layer': 'MMT_270_RVO_SSS_Contact_Listing_PNT',
        'show': False,
        'point_style': {'radius': 3, 'color': 'cyan', 'fillColor': 'cyan', 'fillOpacity': 0.5},
        'popup_fields': ['ID'],
    },
    'mag_anomalies': {
        'name': 'Magnetometer Anomalies',
        'gdb_layer': 'MMT_270_RVO_MAG_Anomaly_Listing_PNT',
        'show': False,
        'point_style': {'radius': 3, 'color': 'magenta', 'fillColor': 'magenta', 'fillOpacity': 0.5},
        'popup_fields': ['ID'],
    },
    'sss_boulders': {
        'name': 'Isolated Boulders',
        'gdb_layer': 'MMT_270_RVO_SSS_Isolated_Boulder_Listing_PNT',
        'show': False,
        'point_style': {'radius': 4, 'color': 'gray', 'fillColor': 'gray', 'fillOpacity': 0.6},
        'popup_fields': ['ID'],
    },
    'integrated_contacts': {
        'name': 'Integrated SSS/MAG Contacts',
        'gdb_layer': 'MMT_270_RVO_Intergrated_SSS_MAG_Contact_Listing_PNT',
        'show': False,
        'point_style': {'radius': 4, 'color': '#FF1493', 'fillColor': '#FF69B4', 'fillOpacity': 0.6},
        'popup_fields': ['ID'],
    },
}

# Dashboard statistics (updated for TNW)
DASHBOARD_STATS = {
    'cables': 128,
    'pipelines': 533,
    'turbines': 294,
    'hazards': 372,
    'total_layers': 79,
}
