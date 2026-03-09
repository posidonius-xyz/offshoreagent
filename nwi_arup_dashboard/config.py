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
        'style': {'fillColor': 'green', 'color': 'darkgreen', 'weight': 3, 'fillOpacity': 0.1, 'dashArray': '10, 5'},
        'popup_fields': [],
    },
    'wind_farm_zones': {
        'name': 'Wind Farm Zones (All)',
        'gdb_layer': 'Wind_Farm_Zones',
        'show': False,
        'style': {'fillColor': 'lightgreen', 'color': 'green', 'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'},
        'popup_fields': ['Naam', 'OBJECTID'],
    },
    'investigation_area': {
        'name': 'Investigation Area',
        'gdb_layer': 'NW_Site_I_Investigation_Area',
        'show': True,
        'style': {'fillColor': 'blue', 'color': 'blue', 'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'},
        'popup_fields': [],
    },

    # === Infrastructure ===
    'cables': {
        'name': 'Cables',
        'gdb_layer': 'Cables',
        'show': True,
        'style': {'color': 'orange', 'weight': 2, 'opacity': 0.8},
        'popup_fields': ['TYPE', 'OWNER', 'NAME', 'CODE'],
    },
    'pipelines': {
        'name': 'Pipelines / Umbilicals',
        'gdb_layer': 'Pipelines_Umbilicals',
        'show': True,
        'style': {'color': 'red', 'weight': 2.5, 'opacity': 0.8},
        'popup_fields': ['NAME_FULL', 'NAME', 'MATERIAL', 'DIA_OUT_INCH', 'OPERATOR'],
    },
    'structures': {
        'name': 'Structures',
        'gdb_layer': 'Structures',
        'show': False,
        'style': {'color': '#8B4513', 'weight': 2, 'opacity': 0.7},
        'popup_fields': [],
    },
    'infrastructure': {
        'name': 'As-found Infrastructure',
        'gdb_layer': 'Infrastructure_As_found_Infrastructure_Arc',
        'show': False,
        'style': {'color': 'brown', 'weight': 1.5, 'opacity': 0.7},
        'popup_fields': [],
    },

    # === Geotechnical ===
    'boreholes': {
        'name': 'Borehole Locations',
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
        'popup_fields': ['Location_ID', 'Final_Depth'],
    },
    'scpt': {
        'name': 'SCPT',
        'gdb_layer': 'SCPT',
        'show': False,
        'point_style': {'radius': 5, 'color': '#FF1493', 'fillColor': '#FF69B4', 'fillOpacity': 0.6},
        'popup_fields': ['Borehole_Sample__TestPoint'],
    },
    'tcpt': {
        'name': 'TCPT',
        'gdb_layer': 'TCPT',
        'show': False,
        'point_style': {'radius': 5, 'color': '#FF4500', 'fillColor': '#FF6347', 'fillOpacity': 0.6},
        'popup_fields': ['Borehole_Sample__TestPoint'],
    },
    'vibrocore': {
        'name': 'VibroCore',
        'gdb_layer': 'VibroCore',
        'show': False,
        'point_style': {'radius': 5, 'color': 'green', 'fillColor': 'lightgreen', 'fillOpacity': 0.6},
        'popup_fields': ['Borehole_Sample__TestPoint'],
    },
    'downhole': {
        'name': 'Downhole Geophysical Measurements',
        'gdb_layer': 'Downhole_Geophysical_Measurements__BGL_',
        'show': False,
        'point_style': {'radius': 7, 'color': 'darkred', 'fillColor': '#DC143C', 'fillOpacity': 0.7},
        'popup_fields': ['Location_ID', 'Final_Depth'],
    },

    # === Geophysical ===
    'mag_contacts': {
        'name': 'Magnetometer Contacts',
        'gdb_layer': 'Geophysical_Survey_Magnetometer_Contacts',
        'show': False,
        'point_style': {'radius': 3, 'color': '#FFD700', 'fillColor': 'gold', 'fillOpacity': 0.5},
        'popup_fields': [],
    },
    'sss_contacts': {
        'name': 'SSS Contacts',
        'gdb_layer': 'Geophysical_Survey_SSS_Contacts',
        'show': False,
        'point_style': {'radius': 3, 'color': '#00CED1', 'fillColor': 'darkturquoise', 'fillOpacity': 0.5},
        'popup_fields': [],
    },
    'sediment_primary': {
        'name': 'Sediment Primary',
        'gdb_layer': 'Geophysical_Survey_Sediment_Primary',
        'show': False,
        'style': {'fillColor': '#DAA520', 'color': '#B8860B', 'weight': 1, 'fillOpacity': 0.3},
        'popup_fields': [],
    },
    'seismic_lines': {
        'name': 'Priority Seismic Lines',
        'gdb_layer': 'Geophysical_Survey_Priority_Seismic_Lines',
        'show': False,
        'style': {'color': '#7B68EE', 'weight': 1.5, 'opacity': 0.6},
        'popup_fields': ['Survey_Lin'],
    },

    # === Geological / Hazards ===
    'faults': {
        'name': 'Faults',
        'gdb_layer': 'Faults',
        'show': True,
        'style': {'color': '#FF0000', 'weight': 3, 'opacity': 0.9, 'dashArray': '8, 4'},
        'popup_fields': [],
    },
    'buried_channels': {
        'name': 'Buried Channels',
        'gdb_layer': 'Buried_channels',
        'show': False,
        'style': {'fillColor': '#8B0000', 'color': '#8B0000', 'weight': 2, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
    'seismic_anomaly': {
        'name': 'Seismic Anomalies',
        'gdb_layer': 'Seismic_anomaly_1',
        'show': False,
        'style': {'fillColor': '#FF6347', 'color': '#FF4500', 'weight': 1, 'fillOpacity': 0.25},
        'popup_fields': [],
    },
    'mtd_above': {
        'name': 'MTDs Above 60m BSF',
        'gdb_layer': 'E3_MTDs_Above_60mBSF',
        'show': False,
        'style': {'fillColor': '#CD853F', 'color': '#A0522D', 'weight': 2, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
    'mtd_below': {
        'name': 'MTDs Below 60m BSF',
        'gdb_layer': 'E3_MTDs_Below_60mBSF',
        'show': False,
        'style': {'fillColor': '#CD853F', 'color': '#A0522D', 'weight': 2, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
    'unit_channels': {
        'name': 'E1 Unit Channels',
        'gdb_layer': 'E_1_Unit_Channels',
        'show': False,
        'style': {'fillColor': '#4682B4', 'color': '#4169E1', 'weight': 2, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
    'mobile_subcrop': {
        'name': 'Mobile Sediments Subcrop Features',
        'gdb_layer': 'MobileSediments_SubcropFeatures',
        'show': False,
        'style': {'fillColor': '#DEB887', 'color': '#D2691E', 'weight': 1.5, 'fillOpacity': 0.25},
        'popup_fields': ['Feature'],
    },
    'mobile_sediments': {
        'name': 'Potential Mobile Sediments',
        'gdb_layer': 'Potential_mobile_sediments',
        'show': False,
        'style': {'fillColor': '#F4A460', 'color': '#D2691E', 'weight': 1.5, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
    'n_tunnel_valley': {
        'name': 'Northern Tunnel Valley Escarpment',
        'gdb_layer': 'NorthernTunnelValley_Escarpment',
        'show': False,
        'style': {'fillColor': '#708090', 'color': '#2F4F4F', 'weight': 2, 'fillOpacity': 0.15},
        'popup_fields': [],
    },
    's_tunnel_valley': {
        'name': 'Southern Tunnel Valley Escarpment',
        'gdb_layer': 'SouthernTunnelValley_Escarpment',
        'show': False,
        'style': {'fillColor': '#708090', 'color': '#2F4F4F', 'weight': 2, 'fillOpacity': 0.15},
        'popup_fields': [],
    },
    'glacio_e4': {
        'name': 'E4 Glaciotectonised Sediments',
        'gdb_layer': 'E_4_Potential_Glaciotectonised_Sediments',
        'show': False,
        'style': {'fillColor': '#B0C4DE', 'color': '#4682B4', 'weight': 2, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
    'glacio_e5': {
        'name': 'E5 Glaciotectonised Sediments',
        'gdb_layer': 'E_5_Potential_Glaciotectonised_Sediments',
        'show': False,
        'style': {'fillColor': '#B0C4DE', 'color': '#4682B4', 'weight': 2, 'fillOpacity': 0.2},
        'popup_fields': [],
    },
}

# Dashboard statistics
DASHBOARD_STATS = {
    'boreholes': 68,
    'geophysical': '6.8K',
    'hazard_features': 35,
    'total_layers': 79,
}
