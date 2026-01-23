# CLAUDE.md

## Project Overview

This is a **GIS Data Processing and Visualization System** template for building interactive web dashboards from geospatial data. The system downloads, inventories, and visualizes data from APIs or local geodatabases, presenting complex geographic information through a Flask-based web dashboard.

**Use Cases:** Infrastructure mapping, environmental monitoring, urban planning, asset management, geological surveys, or any domain requiring geospatial visualization.

### Example Implementation

This project includes an example implementation for Dutch offshore wind farm infrastructure (Nederwiek I), demonstrating the full workflow with geological ground models, infrastructure assets, and survey data from the Pleio DataHub API.

## Agent Execution Guidelines

**IMPORTANT:** Always prefer Docker Compose commands over direct Python execution. This ensures:
- Consistent environment with all GIS dependencies (GDAL, GEOS, Proj)
- Isolated execution without polluting host system
- Pre-configured tools like `azcopy` for data downloads
- Reproducible results across different machines

### Preferred Commands (Docker Compose)

```bash
# Run the dashboard
docker compose up web
# Access at http://localhost:8000

# List available datasets (JSON output for parsing)
docker compose run --rm data-download --json list

# Download specific datasets by ID
docker compose run --rm data-download download --id 123 456

# Download all datasets
docker compose run --rm data-download download --all

# Search datasets
docker compose run --rm data-download --json search "keyword"

# Inventory geodatabase layers
docker compose run --rm gdb-inventory

# Run arbitrary Python scripts
docker compose run --rm python-runner script.py --args
```

**Note:** Global options (`--json`, `--limit`, `--api-base`) must come BEFORE the subcommand.

### Fallback Commands (Local Python)

Only use these if Docker is unavailable:

```bash
# Setup virtual environment
py -3 -m venv venv && venv\Scripts\activate  # Windows
python3 -m venv venv && source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run commands locally
python infrastructure_dashboard.py
python data_download.py list --json
python gdb_inventory.py
```

## Docker Services Reference

| Service | Purpose | Usage |
|---------|---------|-------|
| `web` | Dashboard server | `docker compose up web` |
| `data-download` | Download datasets from API | `docker compose run --rm data-download <command>` |
| `gdb-inventory` | Analyze geodatabase layers | `docker compose run --rm gdb-inventory` |
| `python-runner` | Run arbitrary scripts | `docker compose run --rm python-runner script.py` |

### Data Download Commands

```bash
# List datasets
docker compose run --rm data-download list
docker compose run --rm data-download --json list
docker compose run --rm data-download --limit 100 list

# Get dataset info
docker compose run --rm data-download info --id 123
docker compose run --rm data-download --json info --index 5

# Download datasets
docker compose run --rm data-download download --id 123
docker compose run --rm data-download download --id 123 456 789
docker compose run --rm data-download download --index 1 2 3
docker compose run --rm data-download download --all

# Search
docker compose run --rm data-download search "keyword"
docker compose run --rm data-download --json search "keyword"

# Custom API endpoint
docker compose run --rm data-download --api-base https://other-api.com/v1 list
```

## Project Structure

```
project/
├── infrastructure_dashboard/     # Flask application package
│   ├── __init__.py              # App factory
│   ├── app.py                   # Main entry
│   ├── config.py                # Layer configs, map defaults, data paths
│   ├── data_loader.py           # GIS data loading & CRS transformation
│   ├── map_builder.py           # Folium map creation & layer styling
│   ├── routes.py                # Flask route handlers
│   └── templates/dashboard.html # Dashboard template
├── data_download.py             # CLI for downloading datasets from API
├── gdb_inventory.py             # Inventories geodatabase layers
├── infrastructure_dashboard.py  # Dashboard entry point
├── docker-compose.yml           # Container orchestration
├── Dockerfile                   # Web service image (with GIS libs)
├── Dockerfile.download          # Download service image (with azcopy)
├── data-extracted/              # Extracted geodatabase files
└── data/                        # Downloaded raw archives (git-ignored)
```

## Building a New Dashboard

### Phase 1: Data Acquisition

1. **Identify data source** - API endpoint, geodatabase file, shapefiles, GeoJSON, etc.
2. **Download/obtain data**:
   ```bash
   # List available datasets
   docker compose run --rm data-download --json list

   # Download selected datasets
   docker compose run --rm data-download download --id <dataset_ids>
   ```
3. **Extract archives** - Place geodatabases/shapefiles in `data-extracted/`

### Phase 2: Data Inventory

1. **Run inventory script**:
   ```bash
   docker compose run --rm gdb-inventory
   ```
2. **Document layer types** - Points, lines, polygons, rasters
3. **Identify key fields** - Attributes useful for popups and filtering
4. **Note coordinate system** - Required for CRS transformation

### Phase 3: Configuration

Update `config.py` with:

```python
# Data source path
GDB_PATH = "./data-extracted/your_data.gdb"

# Map center and zoom for your region
MAP_CENTER = [latitude, longitude]
MAP_ZOOM = 10

# Layer definitions
LAYERS = {
    "layer_name": {
        "source": "Layer_Name_In_GDB",
        "style": {"color": "#hex", "weight": 2, "fillOpacity": 0.5},
        "popup_fields": ["field1", "field2"],
        "visible": True
    }
}
```

### Phase 4: Data Loading

Modify `data_loader.py` to handle your data:

1. **Set source CRS** - Update EPSG code for your data's coordinate system
2. **Handle special cases** - Raster layers, multi-geometry, null handling
3. **Add computed fields** - Derive values if needed for display

### Phase 5: Map Building & Deployment

1. Customize `map_builder.py` for visualization
2. Test locally:
   ```bash
   docker compose up web
   ```
3. Access dashboard at http://localhost:8000

## Key Technical Details

### Coordinate Systems

- **Source Data:** Identify your data's CRS (e.g., EPSG:28992, EPSG:32632, EPSG:4269)
- **Web Display:** EPSG:4326 (WGS84) - required for web mapping
- Transformation handled automatically in `data_loader.py` using PyProj

Common CRS codes:
- `EPSG:4326` - WGS84 (GPS coordinates)
- `EPSG:3857` - Web Mercator
- `EPSG:28992` - Dutch RD New
- `EPSG:32632` - UTM Zone 32N (Europe)
- `EPSG:4269` - NAD83 (North America)

### Technologies

- **GIS Stack:** Fiona, GeoPandas, PyProj, GDAL/GEOS
- **Web:** Flask, Folium (Leaflet.js wrapper), Gunicorn
- **Data:** Pandas, Requests
- **Runtime:** Python 3.11+, Docker

### Supported Data Formats

- **Geodatabase:** `.gdb` (Esri File Geodatabase)
- **Shapefile:** `.shp` (with .dbf, .shx, .prj)
- **GeoJSON:** `.geojson`, `.json`
- **GeoPackage:** `.gpkg`
- **KML/KMZ:** `.kml`, `.kmz`

## Development Guidelines

### Code Style

- Flask app follows factory pattern in `infrastructure_dashboard/__init__.py`
- Configuration centralized in `config.py` (layer definitions, map settings)
- GIS data cached at startup for performance
- Graceful error handling for missing/raster layers

### Adding New Layers

1. Define layer in `config.py` with name, style, and popup fields
2. Implement loading logic in `data_loader.py` if special handling needed
3. Add to map in `map_builder.py` with appropriate styling
4. Test: `docker compose run --rm gdb-inventory`

### Routes

- `/` - Main dashboard with header & statistics
- `/map` - Iframe-embedded map only
- `/fullscreen` - Full-screen map view

### Error Handling

- Skip raster layers (not supported by Folium)
- Handle null geometries gracefully
- Log warnings for missing layers rather than failing
- Validate CRS before transformation

## Example: Nederwiek I Dataset

The included example uses Dutch offshore wind farm data:

- **Source:** Pleio DataHub API (public, no auth required)
- **CRS:** EPSG:28992 (RD New - Dutch national grid)
- **Content:** 79 layers with geotechnical, geophysical, geological, hazard, infrastructure, and administrative features
- **GDB Path:** `./data-extracted/RVO_NW_I_GGM.gdb`

Layer categories in this example:
- Geotechnical: Boreholes, PCPT, VibroCore surveys
- Geophysical: Magnetometer, Side-Scan Sonar data
- Geological: Horizon contours, unit boundaries
- Hazards: Faults, buried channels
- Infrastructure: Cables, pipelines, structures
- Administrative: Boundaries, investigation areas

## Documentation

- `AGENTS.md` - Complete GIS workflow guide (5 phases)
- `SETUP.md` - Windows setup instructions
- `datasets_analysis.md` - Available datasets summary (example)
- `gdb_data_inventory.md` - Layer inventory (example)
