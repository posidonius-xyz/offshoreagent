# GIS Notebooks

Interactive Jupyter notebooks for exploring and analyzing geospatial data.

## Getting Started

### Using Docker (Recommended)

```bash
# Start JupyterLab
docker compose up jupyter

# Access at http://localhost:8888
```

### Using Local Python

```bash
# Install dependencies
pip install -r requirements.txt jupyterlab matplotlib

# Start JupyterLab
jupyter lab --notebook-dir=notebooks
```

## Available Notebooks

| Notebook | Description |
|----------|-------------|
| `01_explore_geodatabase.ipynb` | Explore and inventory geodatabase layers, inspect schemas and CRS |
| `02_visualize_layers.ipynb` | Create interactive maps with Folium, add styling and popups |
| `03_spatial_analysis.ipynb` | Perform spatial queries, buffers, distance calculations, and joins |

## Workflow

1. **Explore** - Use `01_explore_geodatabase.ipynb` to understand your data structure
2. **Visualize** - Use `02_visualize_layers.ipynb` to create interactive maps
3. **Analyze** - Use `03_spatial_analysis.ipynb` for spatial operations

## Configuration

Each notebook expects geodatabase files in `../data-extracted/`. Update the `GDB_PATH` variable in each notebook to point to your data:

```python
GDB_PATH = "../data-extracted/your_data.gdb"
```

## Dependencies

- `geopandas` - Geospatial data manipulation
- `fiona` - Reading/writing geospatial data
- `folium` - Interactive map visualization
- `matplotlib` - Static plots
- `pandas` - Data analysis
- `pyproj` - Coordinate transformations
