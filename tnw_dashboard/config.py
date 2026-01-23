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
    },
    'designated_wind_areas': {
        'name': 'Designated Wind Areas',
        'gdb_layer': 'ZDv_aangewez_windgebied_nwp',
        'show': False,
    },
    'wind_farm_buffer': {
        'name': 'Wind Farm Buffer',
        'gdb_layer': 'windparken_buffer',
        'show': False,
    },
    'turbines': {
        'name': 'Wind Turbines',
        'gdb_layer': 'windparken_turbines',
        'show': True,
    },
    # Infrastructure
    'cables': {
        'name': 'Cables',
        'gdb_layer': 'ZDl_electra_telecom_kabels',
        'show': True,
    },
    'cables_buffer': {
        'name': 'Cables Buffer',
        'gdb_layer': 'ZDl_electra_telecom_kabels_buffer',
        'show': False,
    },
    'pipelines': {
        'name': 'Pipelines',
        'gdb_layer': 'ZDl_leidingen',
        'show': True,
    },
    'pipelines_buffer': {
        'name': 'Pipelines Buffer',
        'gdb_layer': 'WOZ_leidingen_buffer_20160217',
        'show': False,
    },
    # Survey Areas
    'survey_boundary': {
        'name': 'Survey Boundary',
        'gdb_layer': 'MMT_270_Survey_Boundary',
        'show': True,
    },
    'project_area': {
        'name': 'Project Area',
        'gdb_layer': 'MMT_270_Project_Area',
        'show': False,
    },
    # Hazards & Geological Features
    'hazards_polygon': {
        'name': 'Hazards (Areas)',
        'gdb_layer': 'MMT_270_RVO_HAZARDS_PGN',
        'show': True,
    },
    'hazards_line': {
        'name': 'Hazards (Linear)',
        'gdb_layer': 'MMT_270_RVO_HAZARDS_LIN',
        'show': False,
    },
    'hazards_point': {
        'name': 'Hazards (Points)',
        'gdb_layer': 'MMT_270_RVO_HAZARDS_PNT',
        'show': False,
    },
    'faults': {
        'name': 'Faults',
        'gdb_layer': 'MMT_270_RVO_FAULTS_LIN',
        'show': True,
    },
    'bedforms': {
        'name': 'Bedforms',
        'gdb_layer': 'MMT_270_RVO_Bedforms_PGN',
        'show': False,
    },
    'sediments': {
        'name': 'Sediments',
        'gdb_layer': 'RVO_MMT_103270_Sediments_PGN',
        'show': False,
    },
    # Survey Data
    'known_objects': {
        'name': 'Known Objects',
        'gdb_layer': 'TNW_Known_Objects',
        'show': True,
    },
    'grab_samples': {
        'name': 'Grab Samples',
        'gdb_layer': 'MMT_270_RVO_Grab_Sample_Listing',
        'show': False,
    },
    'sss_contacts': {
        'name': 'SSS Contacts',
        'gdb_layer': 'MMT_270_RVO_SSS_Contact_Listing_PNT',
        'show': False,
    },
    'mag_anomalies': {
        'name': 'Magnetometer Anomalies',
        'gdb_layer': 'MMT_270_RVO_MAG_Anomaly_Listing_PNT',
        'show': False,
    },
    'sss_boulders': {
        'name': 'Isolated Boulders',
        'gdb_layer': 'MMT_270_RVO_SSS_Isolated_Boulder_Listing_PNT',
        'show': False,
    },
    'integrated_contacts': {
        'name': 'Integrated SSS/MAG Contacts',
        'gdb_layer': 'MMT_270_RVO_Intergrated_SSS_MAG_Contact_Listing_PNT',
        'show': False,
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
