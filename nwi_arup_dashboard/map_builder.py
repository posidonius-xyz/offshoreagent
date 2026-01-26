"""
Map building functions for creating Folium maps with NWI Arup GGM layers
"""

import folium
from folium.plugins import Fullscreen, MeasureControl

from .config import DEFAULT_CENTER_LAT, DEFAULT_CENTER_LON, DEFAULT_ZOOM
from .data_loader import load_all_layers, get_map_center

# Cache for loaded GIS data (loaded once at startup)
_cached_layers = None


def get_layers():
    """Get cached layers, loading them if not already loaded."""
    global _cached_layers
    if _cached_layers is None:
        _cached_layers = load_all_layers()
    return _cached_layers


def create_base_map(center_lat: float, center_lon: float, zoom: int = DEFAULT_ZOOM):
    """Create a base Folium map with multiple basemap options."""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles=None
    )

    folium.TileLayer(
        tiles='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        attr='OpenStreetMap',
        name='OpenStreetMap'
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satellite'
    ).add_to(m)

    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}',
        attr='Esri Ocean',
        name='Ocean Basemap'
    ).add_to(m)

    return m


# ==========================================================================
# Administrative / Boundary Layers
# ==========================================================================

def add_wind_farm_layer(m, gdf, show=True):
    """Add NW Site I Wind Farm Zone."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name='Wind Farm Zone', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'green', 'color': 'darkgreen',
                'weight': 3, 'fillOpacity': 0.1, 'dashArray': '10, 5'
            },
            tooltip='Nederwiek I Wind Farm Zone'
        ).add_to(group)
    group.add_to(m)


def add_wind_farm_zones_layer(m, gdf, show=False):
    """Add all Wind Farm Zones."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Wind Farm Zones ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        name = str(row.get('Naam', row.get('OBJECTID', '')))
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'lightgreen', 'color': 'green',
                'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'
            },
            tooltip=f'Wind Farm Zone: {name}'
        ).add_to(group)
    group.add_to(m)


def add_investigation_area_layer(m, gdf, show=True):
    """Add investigation area layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name='Investigation Area', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'blue', 'color': 'blue',
                'weight': 2, 'fillOpacity': 0.05, 'dashArray': '5, 5'
            },
            tooltip='Investigation Area'
        ).add_to(group)
    group.add_to(m)


# ==========================================================================
# Infrastructure Layers
# ==========================================================================

def add_cables_layer(m, gdf, show=True):
    """Add cables layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Cables ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        cable_type = str(row.get('TYPE', 'N/A'))
        owner = str(row.get('OWNER', 'N/A'))
        name = str(row.get('NAME', row.get('CODE', 'N/A')))

        popup_html = f"<b>Cable</b><br>Type: {cable_type}<br>Owner: {owner}<br>Name: {name}"
        color = 'orange' if cable_type == 'Ct' else 'yellow' if cable_type == 'Cp' else 'gray'

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x, c=color: {'color': c, 'weight': 2, 'opacity': 0.8},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Cable: {name}"
        ).add_to(group)
    group.add_to(m)


def add_pipelines_layer(m, gdf, show=True):
    """Add pipelines/umbilicals layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Pipelines ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        name_full = str(row.get('NAME_FULL', row.get('NAME', 'N/A')))
        material = str(row.get('MATERIAL', 'N/A'))
        diameter = str(row.get('DIA_OUT_INCH', 'N/A'))
        operator = str(row.get('OPERATOR', 'N/A'))

        popup_html = (f"<b>Pipeline/Umbilical</b><br>Name: {name_full}<br>"
                      f"Material: {material}<br>Diameter: {diameter} in<br>Operator: {operator}")

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'red', 'weight': 2.5, 'opacity': 0.8},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Pipeline: {name_full[:30]}"
        ).add_to(group)
    group.add_to(m)


def add_structures_layer(m, gdf, show=False):
    """Add structures layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Structures ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': '#8B4513', 'weight': 2, 'opacity': 0.7},
            tooltip='Structure'
        ).add_to(group)
    group.add_to(m)


def add_infrastructure_layer(m, gdf, show=False):
    """Add as-found infrastructure layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'As-found Infrastructure ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'brown', 'weight': 1.5, 'opacity': 0.7},
            tooltip='As-found Infrastructure'
        ).add_to(group)
    group.add_to(m)


# ==========================================================================
# Geotechnical Layers (Points)
# ==========================================================================

def add_boreholes_layer(m, gdf, show=True):
    """Add borehole locations layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Boreholes ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        bh_id = str(row.get('Borehole_I', row.get('UWI', 'N/A')))
        popup_html = f"<b>Borehole</b><br>ID: {bh_id}"
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=6, color='darkblue', fill=True,
            fillColor='blue', fillOpacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Borehole: {bh_id}"
        ).add_to(group)
    group.add_to(m)


def add_pcpt_layer(m, gdf, show=False):
    """Add PCPT locations layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'PCPT ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        loc_id = str(row.get('Location_ID', 'Unknown'))
        depth = str(row.get('Final_Depth', 'N/A'))
        popup_html = f"<b>PCPT</b><br>ID: {loc_id}<br>Depth: {depth}"
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5, color='purple', fill=True,
            fillColor='purple', fillOpacity=0.6,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"PCPT: {loc_id}"
        ).add_to(group)
    group.add_to(m)


def add_scpt_layer(m, gdf, show=False):
    """Add SCPT locations layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'SCPT ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        loc_id = str(row.get('Borehole_Sample__TestPoint', 'Unknown'))
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5, color='#FF1493', fill=True,
            fillColor='#FF69B4', fillOpacity=0.6,
            tooltip=f"SCPT: {loc_id}"
        ).add_to(group)
    group.add_to(m)


def add_tcpt_layer(m, gdf, show=False):
    """Add TCPT locations layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'TCPT ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        loc_id = str(row.get('Borehole_Sample__TestPoint', 'Unknown'))
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5, color='#FF4500', fill=True,
            fillColor='#FF6347', fillOpacity=0.6,
            tooltip=f"TCPT: {loc_id}"
        ).add_to(group)
    group.add_to(m)


def add_vibrocore_layer(m, gdf, show=False):
    """Add VibroCore locations layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'VibroCore ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        vc_id = str(row.get('Borehole_Sample__TestPoint', 'Unknown'))
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5, color='green', fill=True,
            fillColor='lightgreen', fillOpacity=0.6,
            tooltip=f"VibroCore: {vc_id}"
        ).add_to(group)
    group.add_to(m)


def add_downhole_layer(m, gdf, show=False):
    """Add Downhole Geophysical Measurements layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Downhole Measurements ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        loc_id = str(row.get('Location_ID', 'Unknown'))
        depth = str(row.get('Final_Depth', 'N/A'))
        popup_html = f"<b>Downhole Measurement</b><br>ID: {loc_id}<br>Depth: {depth}"
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=7, color='darkred', fill=True,
            fillColor='#DC143C', fillOpacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Downhole: {loc_id}"
        ).add_to(group)
    group.add_to(m)


# ==========================================================================
# Geophysical Layers
# ==========================================================================

def add_mag_contacts_layer(m, gdf, show=False):
    """Add magnetometer contacts layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Magnetometer Contacts ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3, color='#FFD700', fill=True,
            fillColor='gold', fillOpacity=0.5,
            tooltip='Magnetometer Contact'
        ).add_to(group)
    group.add_to(m)


def add_sss_contacts_layer(m, gdf, show=False):
    """Add SSS contacts layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'SSS Contacts ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3, color='#00CED1', fill=True,
            fillColor='darkturquoise', fillOpacity=0.5,
            tooltip='SSS Contact'
        ).add_to(group)
    group.add_to(m)


def add_sediment_primary_layer(m, gdf, show=False):
    """Add sediment primary classification layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Sediment Primary ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#DAA520', 'color': '#B8860B',
                'weight': 1, 'fillOpacity': 0.3
            },
            tooltip='Sediment Classification'
        ).add_to(group)
    group.add_to(m)


def add_seismic_lines_layer(m, gdf, show=False):
    """Add priority seismic lines layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Seismic Lines ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        line_id = str(row.get('Survey_Lin', 'N/A'))
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': '#7B68EE', 'weight': 1.5, 'opacity': 0.6},
            tooltip=f"Seismic Line: {line_id}"
        ).add_to(group)
    group.add_to(m)


# ==========================================================================
# Geological / Hazard Layers
# ==========================================================================

def add_faults_layer(m, gdf, show=True):
    """Add faults layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Faults ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': '#FF0000', 'weight': 3, 'opacity': 0.9, 'dashArray': '8, 4'},
            tooltip='Fault'
        ).add_to(group)
    group.add_to(m)


def add_buried_channels_layer(m, gdf, show=False):
    """Add buried channels layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name='Buried Channels', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#8B0000', 'color': '#8B0000',
                'weight': 2, 'fillOpacity': 0.2
            },
            tooltip='Buried Channel'
        ).add_to(group)
    group.add_to(m)


def add_seismic_anomaly_layer(m, gdf, show=False):
    """Add seismic anomaly layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Seismic Anomalies ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#FF6347', 'color': '#FF4500',
                'weight': 1, 'fillOpacity': 0.25
            },
            tooltip='Seismic Anomaly'
        ).add_to(group)
    group.add_to(m)


def add_mtd_layer(m, gdf, label, show=False):
    """Add Mass Transport Deposit layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=label, show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#CD853F', 'color': '#A0522D',
                'weight': 2, 'fillOpacity': 0.2
            },
            tooltip=label
        ).add_to(group)
    group.add_to(m)


def add_unit_channels_layer(m, gdf, show=False):
    """Add E1 Unit Channels layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'E1 Unit Channels ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#4682B4', 'color': '#4169E1',
                'weight': 2, 'fillOpacity': 0.2
            },
            tooltip='E1 Unit Channel'
        ).add_to(group)
    group.add_to(m)


def add_mobile_subcrop_layer(m, gdf, show=False):
    """Add mobile sediments subcrop features layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Mobile Sediment Subcrop ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        feature = str(row.get('Feature', 'N/A'))
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#DEB887', 'color': '#D2691E',
                'weight': 1.5, 'fillOpacity': 0.25
            },
            tooltip=f'Mobile Sediment: {feature}'
        ).add_to(group)
    group.add_to(m)


def add_mobile_sediments_layer(m, gdf, show=False):
    """Add potential mobile sediments layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=f'Potential Mobile Sediments ({len(gdf)})', show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#F4A460', 'color': '#D2691E',
                'weight': 1.5, 'fillOpacity': 0.2
            },
            tooltip='Potential Mobile Sediment'
        ).add_to(group)
    group.add_to(m)


def add_tunnel_valley_layer(m, gdf, label, show=False):
    """Add tunnel valley escarpment layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=label, show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#708090', 'color': '#2F4F4F',
                'weight': 2, 'fillOpacity': 0.15
            },
            tooltip=label
        ).add_to(group)
    group.add_to(m)


def add_glaciotectonised_layer(m, gdf, label, show=False):
    """Add glaciotectonised sediments layer."""
    if gdf is None or len(gdf) == 0:
        return
    group = folium.FeatureGroup(name=label, show=show)
    for _, row in gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#B0C4DE', 'color': '#4682B4',
                'weight': 2, 'fillOpacity': 0.2
            },
            tooltip=label
        ).add_to(group)
    group.add_to(m)


# ==========================================================================
# Map Controls & Assembly
# ==========================================================================

def add_map_controls(m):
    """Add controls to the map (layer control, fullscreen, measure)."""
    folium.LayerControl(collapsed=False).add_to(m)
    Fullscreen().add_to(m)
    MeasureControl(position='topleft').add_to(m)


def create_map():
    """Create the complete interactive Folium map with all layers."""
    layers = get_layers()

    center_lat, center_lon = get_map_center(
        layers.get('wind_farm'),
        DEFAULT_CENTER_LAT,
        DEFAULT_CENTER_LON
    )

    m = create_base_map(center_lat, center_lon)

    # Administrative
    add_wind_farm_layer(m, layers.get('wind_farm'))
    add_wind_farm_zones_layer(m, layers.get('wind_farm_zones'))
    add_investigation_area_layer(m, layers.get('investigation_area'))

    # Infrastructure
    add_cables_layer(m, layers.get('cables'))
    add_pipelines_layer(m, layers.get('pipelines'))
    add_structures_layer(m, layers.get('structures'))
    add_infrastructure_layer(m, layers.get('infrastructure'))

    # Geotechnical
    add_boreholes_layer(m, layers.get('boreholes'))
    add_pcpt_layer(m, layers.get('pcpt'))
    add_scpt_layer(m, layers.get('scpt'))
    add_tcpt_layer(m, layers.get('tcpt'))
    add_vibrocore_layer(m, layers.get('vibrocore'))
    add_downhole_layer(m, layers.get('downhole'))

    # Geophysical
    add_mag_contacts_layer(m, layers.get('mag_contacts'))
    add_sss_contacts_layer(m, layers.get('sss_contacts'))
    add_sediment_primary_layer(m, layers.get('sediment_primary'))
    add_seismic_lines_layer(m, layers.get('seismic_lines'))

    # Geological / Hazards
    add_faults_layer(m, layers.get('faults'))
    add_buried_channels_layer(m, layers.get('buried_channels'))
    add_seismic_anomaly_layer(m, layers.get('seismic_anomaly'))
    add_mtd_layer(m, layers.get('mtd_above'), 'MTDs Above 60m BSF')
    add_mtd_layer(m, layers.get('mtd_below'), 'MTDs Below 60m BSF')
    add_unit_channels_layer(m, layers.get('unit_channels'))
    add_mobile_subcrop_layer(m, layers.get('mobile_subcrop'))
    add_mobile_sediments_layer(m, layers.get('mobile_sediments'))
    add_tunnel_valley_layer(m, layers.get('n_tunnel_valley'), 'N. Tunnel Valley Escarpment')
    add_tunnel_valley_layer(m, layers.get('s_tunnel_valley'), 'S. Tunnel Valley Escarpment')
    add_glaciotectonised_layer(m, layers.get('glacio_e4'), 'E4 Glaciotectonised Sediments')
    add_glaciotectonised_layer(m, layers.get('glacio_e5'), 'E5 Glaciotectonised Sediments')

    add_map_controls(m)

    return m
