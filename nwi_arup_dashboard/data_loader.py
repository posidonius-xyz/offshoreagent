"""
Data loading functions for GIS data from geodatabase files
"""

import warnings
import geopandas as gpd
import pandas as pd

from .config import GDB_PATH, LAYER_CONFIGS

warnings.filterwarnings('ignore')

# Per-layer cache
_layer_cache = {}


def safe_load(gdb_path: str, layer_name: str):
    """
    Safely load a GIS layer from a geodatabase, handling geometry errors.
    """
    try:
        gdf = gpd.read_file(gdb_path, layer=layer_name)
        gdf = gdf[gdf.geometry.is_valid]
        gdf = gdf[~gdf.geometry.is_empty]

        if gdf.crs and gdf.crs != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        for col in gdf.columns:
            if pd.api.types.is_datetime64_any_dtype(gdf[col]):
                gdf[col] = gdf[col].astype(str)

        return gdf
    except Exception as e:
        print(f"Warning: Could not load {layer_name}: {e}")
        return None


def load_single_layer(key, gdb_path=None):
    """Load a single layer by key with caching."""
    if key in _layer_cache:
        return _layer_cache[key]

    if key not in LAYER_CONFIGS:
        return None

    if gdb_path is None:
        gdb_path = GDB_PATH

    config = LAYER_CONFIGS[key]
    gdf = safe_load(gdb_path, config['gdb_layer'])
    _layer_cache[key] = gdf
    return gdf


def load_all_layers(gdb_path: str = None):
    """Load all configured layers from the geodatabase."""
    if gdb_path is None:
        gdb_path = GDB_PATH

    print("Loading GIS data...")

    layers = {}
    for key, config in LAYER_CONFIGS.items():
        layers[key] = load_single_layer(key, gdb_path)

    return layers


def get_map_center(wind_farm_gdf, default_lat: float = 52.5, default_lon: float = 4.0):
    """Calculate map center from wind farm zone bounds."""
    if wind_farm_gdf is not None and len(wind_farm_gdf) > 0:
        bounds = wind_farm_gdf.total_bounds
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        return center_lat, center_lon

    return default_lat, default_lon
