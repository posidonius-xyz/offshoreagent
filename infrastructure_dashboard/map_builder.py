"""
Map building functions for creating Folium maps with infrastructure layers
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
    """
    Create a base Folium map with multiple basemap options.

    Args:
        center_lat: Center latitude
        center_lon: Center longitude
        zoom: Initial zoom level

    Returns:
        Folium Map object
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles=None
    )

    # Add basemap options
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


def add_wind_farm_layer(m, wind_farm_gdf, show: bool = True):
    """Add wind farm zone layer to the map."""
    if wind_farm_gdf is None or len(wind_farm_gdf) == 0:
        return

    group = folium.FeatureGroup(name='Wind Farm Zone', show=show)
    for _, row in wind_farm_gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'green',
                'color': 'darkgreen',
                'weight': 3,
                'fillOpacity': 0.1,
                'dashArray': '10, 5'
            },
            tooltip='Nederwiek I Wind Farm Zone'
        ).add_to(group)
    group.add_to(m)


def add_investigation_area_layer(m, investigation_gdf, show: bool = False):
    """Add investigation area layer to the map."""
    if investigation_gdf is None or len(investigation_gdf) == 0:
        return

    group = folium.FeatureGroup(name='Investigation Area', show=show)
    for _, row in investigation_gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'blue',
                'color': 'blue',
                'weight': 2,
                'fillOpacity': 0.05,
                'dashArray': '5, 5'
            },
            tooltip='Investigation Area'
        ).add_to(group)
    group.add_to(m)


def add_cables_layer(m, cables_gdf, show: bool = True):
    """Add cables layer to the map."""
    if cables_gdf is None or len(cables_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Cables ({len(cables_gdf)})', show=show)
    for _, row in cables_gdf.iterrows():
        cable_type = str(row.get('TYPE', 'N/A'))
        owner = str(row.get('OWNER', 'N/A'))
        status = str(row.get('STATUS', 'N/A'))
        name = str(row.get('NAME', 'N/A'))

        popup_html = f"""
        <b>Cable</b><br>
        Type: {cable_type}<br>
        Owner: {owner}<br>
        Status: {status}<br>
        Name: {name}
        """

        color = 'orange' if cable_type == 'Ct' else 'yellow' if cable_type == 'Cp' else 'gray'

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x, c=color: {'color': c, 'weight': 2, 'opacity': 0.8},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Cable: {name}"
        ).add_to(group)
    group.add_to(m)


def add_pipelines_layer(m, pipelines_gdf, show: bool = True):
    """Add pipelines/umbilicals layer to the map."""
    if pipelines_gdf is None or len(pipelines_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Pipelines/Umbilicals ({len(pipelines_gdf)})', show=show)
    for _, row in pipelines_gdf.iterrows():
        name_full = str(row.get('NAME_FULL', row.get('NAME', 'N/A')))
        material = str(row.get('MATERIAL', 'N/A'))
        diameter = str(row.get('DIA_OUT_INCH', 'N/A'))
        status = str(row.get('STATUS', 'N/A'))
        operator = str(row.get('OPERATOR', 'N/A'))

        popup_html = f"""
        <b>Pipeline/Umbilical</b><br>
        Name: {name_full}<br>
        Material: {material}<br>
        Diameter: {diameter} inch<br>
        Status: {status}<br>
        Operator: {operator}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'red', 'weight': 2.5, 'opacity': 0.8},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Pipeline: {name_full[:30]}"
        ).add_to(group)
    group.add_to(m)


def add_infrastructure_layer(m, infrastructure_gdf, show: bool = False):
    """Add as-found infrastructure layer to the map."""
    if infrastructure_gdf is None or len(infrastructure_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'As-found Infrastructure ({len(infrastructure_gdf)})', show=show)
    for _, row in infrastructure_gdf.iterrows():
        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'brown', 'weight': 1.5, 'opacity': 0.7},
            tooltip='As-found Infrastructure'
        ).add_to(group)
    group.add_to(m)


def add_boreholes_layer(m, boreholes_gdf, show: bool = True):
    """Add boreholes layer to the map."""
    if boreholes_gdf is None or len(boreholes_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Boreholes ({len(boreholes_gdf)})', show=show)
    for _, row in boreholes_gdf.iterrows():
        bh_id = str(row.get('Borehole_I', row.get('UWI', 'N/A')))
        popup_html = f"<b>Borehole</b><br>ID: {bh_id}"

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=6,
            color='darkblue',
            fill=True,
            fillColor='blue',
            fillOpacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Borehole: {bh_id}"
        ).add_to(group)
    group.add_to(m)


def add_pcpt_layer(m, pcpt_gdf, show: bool = False):
    """Add PCPT locations layer to the map."""
    if pcpt_gdf is None or len(pcpt_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'PCPT ({len(pcpt_gdf)})', show=show)
    for _, row in pcpt_gdf.iterrows():
        loc_id = str(row.get('Location_ID', 'Unknown'))
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5,
            color='purple',
            fill=True,
            fillColor='purple',
            fillOpacity=0.6,
            tooltip=f"PCPT: {loc_id}"
        ).add_to(group)
    group.add_to(m)


def add_vibrocore_layer(m, vibrocore_gdf, show: bool = False):
    """Add VibroCore locations layer to the map."""
    if vibrocore_gdf is None or len(vibrocore_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'VibroCore ({len(vibrocore_gdf)})', show=show)
    for _, row in vibrocore_gdf.iterrows():
        vc_id = str(row.get('Borehole_Sample__TestPoint', 'Unknown'))
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5,
            color='green',
            fill=True,
            fillColor='lightgreen',
            fillOpacity=0.6,
            tooltip=f"VibroCore: {vc_id}"
        ).add_to(group)
    group.add_to(m)


def add_map_controls(m):
    """Add controls to the map (layer control, fullscreen, measure)."""
    folium.LayerControl(collapsed=False).add_to(m)
    Fullscreen().add_to(m)
    MeasureControl(position='topleft').add_to(m)


def create_map():
    """
    Create the complete interactive Folium map with all layers.

    Returns:
        Folium Map object
    """
    # Get cached data layers
    layers = get_layers()

    # Calculate map center from wind farm zone
    center_lat, center_lon = get_map_center(
        layers.get('wind_farm'),
        DEFAULT_CENTER_LAT,
        DEFAULT_CENTER_LON
    )

    # Create base map
    m = create_base_map(center_lat, center_lon)

    # Add all layers
    add_wind_farm_layer(m, layers.get('wind_farm'))
    add_investigation_area_layer(m, layers.get('investigation_area'))
    add_cables_layer(m, layers.get('cables'))
    add_pipelines_layer(m, layers.get('pipelines'))
    add_infrastructure_layer(m, layers.get('infrastructure'))
    add_boreholes_layer(m, layers.get('boreholes'))
    add_pcpt_layer(m, layers.get('pcpt'))
    add_vibrocore_layer(m, layers.get('vibrocore'))

    # Add controls
    add_map_controls(m)

    return m
