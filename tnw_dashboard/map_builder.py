"""
Map building functions for creating Folium maps with TNW infrastructure layers
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


def add_wind_farms_layer(m, wind_farms_gdf, show: bool = True):
    """Add wind farm zones layer to the map."""
    if wind_farms_gdf is None or len(wind_farms_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Wind Farm Zones ({len(wind_farms_gdf)})', show=show)
    for _, row in wind_farms_gdf.iterrows():
        name = str(row.get('NAAM', row.get('NAME', 'Wind Farm')))
        owner = str(row.get('EIGENAAR', 'N/A'))
        status = str(row.get('STATUS', 'N/A'))

        popup_html = f"""
        <b>Wind Farm Zone</b><br>
        Name: {name}<br>
        Owner: {owner}<br>
        Status: {status}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'green',
                'color': 'darkgreen',
                'weight': 3,
                'fillOpacity': 0.15,
                'dashArray': '10, 5'
            },
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f'Wind Farm: {name}'
        ).add_to(group)
    group.add_to(m)


def add_survey_boundary_layer(m, boundary_gdf, show: bool = True):
    """Add survey boundary layer to the map."""
    if boundary_gdf is None or len(boundary_gdf) == 0:
        return

    group = folium.FeatureGroup(name='Survey Boundary', show=show)
    for _, row in boundary_gdf.iterrows():
        survey_id = str(row.get('SURVEY_ID', 'N/A'))
        comment = str(row.get('COMMENT', ''))

        popup_html = f"""
        <b>Survey Boundary</b><br>
        Survey ID: {survey_id}<br>
        Comment: {comment}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': 'lightblue',
                'color': 'blue',
                'weight': 2,
                'fillOpacity': 0.1,
                'dashArray': '5, 5'
            },
            popup=folium.Popup(popup_html, max_width=300),
            tooltip='Survey Boundary'
        ).add_to(group)
    group.add_to(m)


def add_turbines_layer(m, turbines_gdf, show: bool = True):
    """Add wind turbines layer to the map."""
    if turbines_gdf is None or len(turbines_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Wind Turbines ({len(turbines_gdf)})', show=show)
    for _, row in turbines_gdf.iterrows():
        name = str(row.get('NAAM', 'Turbine'))
        status = str(row.get('STATUS', 'N/A'))

        popup_html = f"""
        <b>Wind Turbine</b><br>
        Name: {name}<br>
        Status: {status}
        """

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=4,
            color='darkgreen',
            fill=True,
            fillColor='#00cc00',
            fillOpacity=0.8,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Turbine: {name}"
        ).add_to(group)
    group.add_to(m)


def add_cables_layer(m, cables_gdf, show: bool = True):
    """Add cables layer to the map."""
    if cables_gdf is None or len(cables_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Cables ({len(cables_gdf)})', show=show)
    for _, row in cables_gdf.iterrows():
        name = str(row.get('NAAM', row.get('NAME', 'N/A')))
        cable_type = str(row.get('KABEL_TYPE', row.get('TYPE', 'N/A')))
        owner = str(row.get('EIGENAAR', row.get('OWNER', 'N/A')))

        popup_html = f"""
        <b>Cable</b><br>
        Name: {name}<br>
        Type: {cable_type}<br>
        Owner: {owner}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'orange', 'weight': 3, 'opacity': 0.8},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Cable: {name}"
        ).add_to(group)
    group.add_to(m)


def add_pipelines_layer(m, pipelines_gdf, show: bool = True):
    """Add pipelines layer to the map."""
    if pipelines_gdf is None or len(pipelines_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Pipelines ({len(pipelines_gdf)})', show=show)
    for _, row in pipelines_gdf.iterrows():
        leid_nr = str(row.get('LEID_NR', 'N/A'))
        pipe_type = str(row.get('TYPE', 'N/A'))
        operator = str(row.get('OPERATOR', 'N/A'))
        status = str(row.get('STATUS', 'N/A'))

        popup_html = f"""
        <b>Pipeline</b><br>
        ID: {leid_nr}<br>
        Type: {pipe_type}<br>
        Operator: {operator}<br>
        Status: {status}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'red', 'weight': 3, 'opacity': 0.8},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Pipeline: {leid_nr}"
        ).add_to(group)
    group.add_to(m)


def add_hazards_polygon_layer(m, hazards_gdf, show: bool = True):
    """Add hazards polygon layer to the map."""
    if hazards_gdf is None or len(hazards_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Hazards - Areas ({len(hazards_gdf)})', show=show)
    for _, row in hazards_gdf.iterrows():
        hazard_type = str(row.get('HAZARD', 'N/A'))
        layer = str(row.get('LAYER', 'N/A'))
        comment = str(row.get('COMMENT', ''))

        popup_html = f"""
        <b>Hazard Area</b><br>
        Type: {hazard_type}<br>
        Layer: {layer}<br>
        Comment: {comment}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {
                'fillColor': '#ffcccc',
                'color': 'red',
                'weight': 2,
                'fillOpacity': 0.4,
            },
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Hazard: {hazard_type}"
        ).add_to(group)
    group.add_to(m)


def add_faults_layer(m, faults_gdf, show: bool = True):
    """Add faults layer to the map."""
    if faults_gdf is None or len(faults_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Faults ({len(faults_gdf)})', show=show)
    for _, row in faults_gdf.iterrows():
        hazard = str(row.get('HAZARD', 'Fault'))
        comment = str(row.get('COMMENT', ''))

        popup_html = f"""
        <b>Fault</b><br>
        Type: {hazard}<br>
        Comment: {comment}
        """

        folium.GeoJson(
            row.geometry.__geo_interface__,
            style_function=lambda x: {'color': 'brown', 'weight': 3, 'opacity': 0.9, 'dashArray': '5, 3'},
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Fault: {hazard}"
        ).add_to(group)
    group.add_to(m)


def add_known_objects_layer(m, objects_gdf, show: bool = True):
    """Add known objects layer to the map."""
    if objects_gdf is None or len(objects_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Known Objects ({len(objects_gdf)})', show=show)
    for _, row in objects_gdf.iterrows():
        ncn = str(row.get('NCN', 'N/A'))
        dhy = str(row.get('DHY', 'N/A'))

        popup_html = f"""
        <b>Known Object</b><br>
        NCN: {ncn}<br>
        DHY: {dhy}
        """

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=7,
            color='darkviolet',
            fill=True,
            fillColor='purple',
            fillOpacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Known Object: {ncn}"
        ).add_to(group)
    group.add_to(m)


def add_grab_samples_layer(m, samples_gdf, show: bool = False):
    """Add grab samples layer to the map."""
    if samples_gdf is None or len(samples_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'Grab Samples ({len(samples_gdf)})', show=show)
    for _, row in samples_gdf.iterrows():
        sample_id = str(row.get('ID', 'N/A'))
        description = str(row.get('DESCRIPTION', ''))

        popup_html = f"""
        <b>Grab Sample</b><br>
        ID: {sample_id}<br>
        Description: {description}
        """

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5,
            color='darkorange',
            fill=True,
            fillColor='orange',
            fillOpacity=0.7,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"Grab Sample: {sample_id}"
        ).add_to(group)
    group.add_to(m)


def add_mag_anomalies_layer(m, anomalies_gdf, show: bool = False):
    """Add magnetometer anomalies layer to the map."""
    if anomalies_gdf is None or len(anomalies_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'MAG Anomalies ({len(anomalies_gdf)})', show=show)
    for _, row in anomalies_gdf.iterrows():
        anomaly_id = str(row.get('ID', 'N/A'))

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3,
            color='magenta',
            fill=True,
            fillColor='magenta',
            fillOpacity=0.5,
            tooltip=f"MAG Anomaly: {anomaly_id}"
        ).add_to(group)
    group.add_to(m)


def add_sss_contacts_layer(m, contacts_gdf, show: bool = False):
    """Add SSS contacts layer to the map."""
    if contacts_gdf is None or len(contacts_gdf) == 0:
        return

    group = folium.FeatureGroup(name=f'SSS Contacts ({len(contacts_gdf)})', show=show)
    for _, row in contacts_gdf.iterrows():
        contact_id = str(row.get('ID', 'N/A'))

        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=3,
            color='cyan',
            fill=True,
            fillColor='cyan',
            fillOpacity=0.5,
            tooltip=f"SSS Contact: {contact_id}"
        ).add_to(group)
    group.add_to(m)


def add_map_controls(m):
    """Add controls to the map (layer control, fullscreen, measure)."""
    folium.LayerControl(collapsed=False).add_to(m)
    Fullscreen().add_to(m)
    MeasureControl(position='topleft').add_to(m)


def create_map():
    """
    Create the complete interactive Folium map with all TNW layers.

    Returns:
        Folium Map object
    """
    # Get cached data layers
    layers = get_layers()

    # Calculate map center from wind farm zones
    center_lat, center_lon = get_map_center(
        layers.get('wind_farms'),
        DEFAULT_CENTER_LAT,
        DEFAULT_CENTER_LON
    )

    # Create base map
    m = create_base_map(center_lat, center_lon)

    # Add all layers (order matters for z-index)
    add_survey_boundary_layer(m, layers.get('survey_boundary'))
    add_wind_farms_layer(m, layers.get('wind_farms'))
    add_hazards_polygon_layer(m, layers.get('hazards_polygon'))
    add_pipelines_layer(m, layers.get('pipelines'))
    add_cables_layer(m, layers.get('cables'))
    add_faults_layer(m, layers.get('faults'))
    add_turbines_layer(m, layers.get('turbines'))
    add_known_objects_layer(m, layers.get('known_objects'))
    add_grab_samples_layer(m, layers.get('grab_samples'))
    add_mag_anomalies_layer(m, layers.get('mag_anomalies'))
    add_sss_contacts_layer(m, layers.get('sss_contacts'))

    # Add controls
    add_map_controls(m)

    return m
