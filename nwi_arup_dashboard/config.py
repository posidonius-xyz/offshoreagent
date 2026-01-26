"""
Configuration constants for the NWI Arup Geological Ground Model Dashboard
"""

import os

# GDB file path (relative to project root)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GDB_PATH = os.path.join(_PROJECT_ROOT, "data-extracted", "NWI_GGM_Arup", "RVO_NW_I_GGM.gdb")

# Default map center (Nederwiek I - North Sea)
DEFAULT_CENTER_LAT = 52.5
DEFAULT_CENTER_LON = 4.0
DEFAULT_ZOOM = 10

# Layer configurations organized by category
LAYER_CONFIGS = {
    # === Administrative / Boundaries ===
    'wind_farm': {
        'name': 'NW Site I Wind Farm Zone',
        'gdb_layer': 'NW_Site_I_Wind_Farm_Zone',
        'show': True,
    },
    'wind_farm_zones': {
        'name': 'Wind Farm Zones (All)',
        'gdb_layer': 'Wind_Farm_Zones',
        'show': False,
    },
    'investigation_area': {
        'name': 'Investigation Area',
        'gdb_layer': 'NW_Site_I_Investigation_Area',
        'show': True,
    },

    # === Infrastructure ===
    'cables': {
        'name': 'Cables',
        'gdb_layer': 'Cables',
        'show': True,
    },
    'pipelines': {
        'name': 'Pipelines / Umbilicals',
        'gdb_layer': 'Pipelines_Umbilicals',
        'show': True,
    },
    'structures': {
        'name': 'Structures',
        'gdb_layer': 'Structures',
        'show': False,
    },
    'infrastructure': {
        'name': 'As-found Infrastructure',
        'gdb_layer': 'Infrastructure_As_found_Infrastructure_Arc',
        'show': False,
    },

    # === Geotechnical ===
    'boreholes': {
        'name': 'Borehole Locations',
        'gdb_layer': 'Borehole_locations',
        'show': True,
    },
    'pcpt': {
        'name': 'PCPT',
        'gdb_layer': 'PCPT',
        'show': False,
    },
    'scpt': {
        'name': 'SCPT',
        'gdb_layer': 'SCPT',
        'show': False,
    },
    'tcpt': {
        'name': 'TCPT',
        'gdb_layer': 'TCPT',
        'show': False,
    },
    'vibrocore': {
        'name': 'VibroCore',
        'gdb_layer': 'VibroCore',
        'show': False,
    },
    'downhole': {
        'name': 'Downhole Geophysical Measurements',
        'gdb_layer': 'Downhole_Geophysical_Measurements__BGL_',
        'show': False,
    },

    # === Geophysical ===
    'mag_contacts': {
        'name': 'Magnetometer Contacts',
        'gdb_layer': 'Geophysical_Survey_Magnetometer_Contacts',
        'show': False,
    },
    'sss_contacts': {
        'name': 'SSS Contacts',
        'gdb_layer': 'Geophysical_Survey_SSS_Contacts',
        'show': False,
    },
    'sediment_primary': {
        'name': 'Sediment Primary',
        'gdb_layer': 'Geophysical_Survey_Sediment_Primary',
        'show': False,
    },
    'seismic_lines': {
        'name': 'Priority Seismic Lines',
        'gdb_layer': 'Geophysical_Survey_Priority_Seismic_Lines',
        'show': False,
    },

    # === Geological / Hazards ===
    'faults': {
        'name': 'Faults',
        'gdb_layer': 'Faults',
        'show': True,
    },
    'buried_channels': {
        'name': 'Buried Channels',
        'gdb_layer': 'Buried_channels',
        'show': False,
    },
    'seismic_anomaly': {
        'name': 'Seismic Anomalies',
        'gdb_layer': 'Seismic_anomaly_1',
        'show': False,
    },
    'mtd_above': {
        'name': 'MTDs Above 60m BSF',
        'gdb_layer': 'E3_MTDs_Above_60mBSF',
        'show': False,
    },
    'mtd_below': {
        'name': 'MTDs Below 60m BSF',
        'gdb_layer': 'E3_MTDs_Below_60mBSF',
        'show': False,
    },
    'unit_channels': {
        'name': 'E1 Unit Channels',
        'gdb_layer': 'E_1_Unit_Channels',
        'show': False,
    },
    'mobile_subcrop': {
        'name': 'Mobile Sediments Subcrop Features',
        'gdb_layer': 'MobileSediments_SubcropFeatures',
        'show': False,
    },
    'mobile_sediments': {
        'name': 'Potential Mobile Sediments',
        'gdb_layer': 'Potential_mobile_sediments',
        'show': False,
    },
    'n_tunnel_valley': {
        'name': 'Northern Tunnel Valley Escarpment',
        'gdb_layer': 'NorthernTunnelValley_Escarpment',
        'show': False,
    },
    's_tunnel_valley': {
        'name': 'Southern Tunnel Valley Escarpment',
        'gdb_layer': 'SouthernTunnelValley_Escarpment',
        'show': False,
    },
    'glacio_e4': {
        'name': 'E4 Glaciotectonised Sediments',
        'gdb_layer': 'E_4_Potential_Glaciotectonised_Sediments',
        'show': False,
    },
    'glacio_e5': {
        'name': 'E5 Glaciotectonised Sediments',
        'gdb_layer': 'E_5_Potential_Glaciotectonised_Sediments',
        'show': False,
    },
}

# Dashboard statistics
DASHBOARD_STATS = {
    'boreholes': 68,
    'geophysical': '6.8K',
    'hazard_features': 35,
    'total_layers': 79,
}
