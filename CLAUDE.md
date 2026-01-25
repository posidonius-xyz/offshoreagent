# CLAUDE.md

## Project Overview

This is a **GIS Data Processing and Visualization System** template for building interactive web dashboards from geospatial data. The system downloads, inventories, and visualizes data from APIs or local geodatabases, presenting complex geographic information through a Flask-based web dashboard.

**Use Cases:** Infrastructure mapping, environmental monitoring, urban planning, asset management, geological surveys, or any domain requiring geospatial visualization.

### Example Implementation

This project includes an example implementation for Dutch offshore wind farm infrastructure (Nederwiek I), demonstrating the full workflow with geological ground models, infrastructure assets, and survey data from the Pleio DataHub API.

## User Preferences

**Dashboard Creation:** When creating new dashboards for different locations/datasets:
- **Create a new directory** for each dashboard (e.g., `tnw_dashboard/`, `nwz_dashboard/`)
- **Use the existing `infrastructure_dashboard/` as a template** - copy and modify
- **Add a new Docker service** in `docker-compose.yml` with a unique port
- **Create a dedicated Dockerfile** (e.g., `Dockerfile.tnw`) for each dashboard
- **Never modify the original `infrastructure_dashboard/`** - keep it as reference

## Agent Execution Guidelines

**IMPORTANT:** Always prefer Docker Compose commands over direct Python execution. This ensures:
- Consistent environment with all GIS dependencies (GDAL, GEOS, Proj)
- Isolated execution without polluting host system
- Pre-configured tools like `azcopy` for data downloads
- Reproducible results across different machines

### Preferred Commands (Docker Compose)

```bash
# Run dashboards
docker compose up nwi-dashboard    # Nederwiek I at http://localhost:8000
docker compose up tnw-dashboard    # TNW at http://localhost:8001

# Run JupyterLab for interactive GIS notebooks
docker compose up jupyter          # JupyterLab at http://localhost:8888

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

| Service | Purpose | Port | Usage |
|---------|---------|------|-------|
| `nwi-dashboard` | Nederwiek I dashboard | 8000 | `docker compose up nwi-dashboard` |
| `tnw-dashboard` | TNW dashboard | 8001 | `docker compose up tnw-dashboard` |
| `jupyter` | JupyterLab for GIS notebooks | 8888 | `docker compose up jupyter` |
| `data-download` | Download datasets from API | - | `docker compose run --rm data-download <command>` |
| `gdb-inventory` | Analyze geodatabase layers | - | `docker compose run --rm gdb-inventory` |
| `python-runner` | Run arbitrary scripts | - | `docker compose run --rm python-runner script.py` |

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
├── infrastructure_dashboard/     # NWI Flask application (reference template)
│   ├── __init__.py              # App factory
│   ├── app.py                   # Main entry
│   ├── config.py                # Layer configs, map defaults, data paths
│   ├── data_loader.py           # GIS data loading & CRS transformation
│   ├── map_builder.py           # Folium map creation & layer styling
│   ├── routes.py                # Flask route handlers
│   └── templates/dashboard.html # Dashboard template
├── tnw_dashboard/               # TNW Flask application (example new dashboard)
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── data_loader.py
│   ├── map_builder.py
│   ├── routes.py
│   └── templates/dashboard.html
├── notebooks/                   # Jupyter notebooks for GIS exploration
│   ├── 01_explore_geodatabase.ipynb   # Inventory and explore GDB layers
│   ├── 02_visualize_layers.ipynb      # Interactive map visualization
│   └── 03_spatial_analysis.ipynb      # Spatial queries and analysis
├── data_download.py             # CLI for downloading datasets from API
├── gdb_inventory.py             # Inventories geodatabase layers
├── infrastructure_dashboard.py  # NWI dashboard entry point
├── tnw_dashboard.py             # TNW dashboard entry point
├── docker-compose.yml           # Container orchestration
├── Dockerfile                   # NWI service image (with GIS libs)
├── Dockerfile.tnw               # TNW service image
├── Dockerfile.jupyter           # JupyterLab service image
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
   docker compose run --rm gdb-inventory ./data-extracted/your_data.gdb
   ```
2. **Document layer types** - Points, lines, polygons, rasters
3. **Identify key fields** - Attributes useful for popups and filtering
4. **Note coordinate system** - Required for CRS transformation

### Phase 3: Create Dashboard Directory

**IMPORTANT:** Create a new directory for each dashboard, using `infrastructure_dashboard/` as template:

```bash
# Create new dashboard directory structure
mkdir -p new_dashboard/templates

# Copy template files
cp infrastructure_dashboard/*.py new_dashboard/
cp infrastructure_dashboard/templates/dashboard.html new_dashboard/templates/
```

### Phase 4: Configuration

Update `new_dashboard/config.py` with:

```python
# Data source path
GDB_PATH = "./data-extracted/your_data.gdb"

# Map center and zoom for your region
DEFAULT_CENTER_LAT = latitude
DEFAULT_CENTER_LON = longitude
DEFAULT_ZOOM = 10

# Layer definitions
LAYER_CONFIGS = {
    "layer_key": {
        "name": "Display Name",
        "gdb_layer": "Layer_Name_In_GDB",
        "show": True,  # Default visibility
    }
}
```

### Phase 5: Customize Map Builder

Modify `new_dashboard/map_builder.py`:

1. **Add layer functions** - One function per layer type with styling
2. **Update `create_map()`** - Call your layer functions
3. **Set popup fields** - Configure what shows on click

### Phase 6: Docker Setup

1. **Create Dockerfile** (e.g., `Dockerfile.new`):
   ```dockerfile
   # Copy from Dockerfile, update COPY paths for new_dashboard/
   COPY new_dashboard/ ./new_dashboard/
   COPY new_dashboard.py .
   CMD ["gunicorn", "...", "new_dashboard:app"]
   ```

2. **Add service to docker-compose.yml**:
   ```yaml
   new-dashboard:
     build:
       context: .
       dockerfile: Dockerfile.new
     ports:
       - "8002:8000"  # Use unique port
     volumes:
       - ./data-extracted:/app/data-extracted:ro
   ```

3. **Create entry point** (`new_dashboard.py`):
   ```python
   from new_dashboard import create_app
   app = create_app()
   ```

### Phase 7: Test & Deploy

```bash
docker compose build new-dashboard
docker compose up new-dashboard
# Access at http://localhost:8002
```

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
