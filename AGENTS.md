# GIS Data Processing Workflow

A repeatable process for downloading, analyzing, and visualizing GIS datasets from data portals.

---

## Phase 1: Data Discovery & Download

### 1.1 Query the Data API

- Use `curl` or `wget` with appropriate headers (`Accept: application/json`)
- Save response to a JSON file for exploration
- Apply query parameters for filtering (limit, classification, zone, etc.)

### 1.2 Analyze Available Datasets

- Parse JSON response to understand data structure
- Identify relevant fields: id, name, size, zone, study type, file format
- Group datasets by category (study type, geographic zone, file format)
- Calculate total sizes to plan storage requirements

### 1.3 Obtain Download URLs

- Many data portals use time-limited tokens (SAS tokens for Azure, presigned URLs for S3)
- Fetch fresh download URLs immediately before downloading
- Check for download endpoints that provide ready-to-use commands

### 1.4 Download Large Files

- Use specialized tools for large files: `azcopy` (Azure), `aws s3 cp` (AWS), `gsutil` (GCP)
- These tools support resume on failure, parallel transfers, and integrity checks
- Avoid browser downloads for files > 1GB

---

## Phase 2: Data Extraction & Organization

### 2.1 Extract Archives

- Use 7-Zip for cross-format support (ZIP, RAR, 7Z, GZ, TAR)
- Extract to a dedicated directory (e.g., `./data-extracted/`)
- Preserve directory structure within archives

### 2.2 Verify Extraction

- Check file counts match expected values
- Verify no extraction errors occurred
- Note file types present (GDB, SHP, GeoJSON, rasters, etc.)

### 2.3 Directory Organization

```
project/
├── datasets.json           # API response
├── datasets_analysis.md    # Summary document
├── data-extracted/         # Extracted GIS data
│   └── *.gdb              # File geodatabases
├── gdb_inventory.py        # Inventory script
├── gdb_inventory.json      # Layer metadata
├── visualize.py            # Visualization script
└── dashboard.py            # Interactive dashboard
```

---

## Phase 3: GIS Data Inventory

### 3.1 Python Libraries

| Library | Purpose |
|---------|---------|
| fiona | Low-level vector data access, layer listing |
| geopandas | High-level vector data manipulation |
| rasterio | Raster data access |
| pyproj | Coordinate reference system handling |

### 3.2 Inventory Best Practices

- List all layers before loading data
- For each layer, capture:
  - Layer name
  - Geometry type (Point, LineString, Polygon, etc.)
  - Feature count
  - Coordinate reference system (CRS)
  - Field names and types
  - Bounding box
- Handle errors gracefully (some layers may be rasters or system tables)
- Export inventory to both JSON (machine-readable) and Markdown (human-readable)

### 3.3 Data Quality Checks

- Filter invalid geometries before processing
- Remove empty geometries
- Check for null values in key fields
- Validate CRS is defined

---

## Phase 4: Static Visualization

### 4.1 Best Practices

- Use `matplotlib` with `geopandas.plot()` for static maps
- Create overview maps showing all layers
- Create detail maps for specific layer categories
- Use consistent color schemes across related layers
- Include:
  - Title and subtitle
  - Legend
  - Scale bar
  - North arrow (if relevant)
  - Grid lines
  - Coordinate labels

### 4.2 Layer Styling Guidelines

| Geometry Type | Recommended Style |
|---------------|-------------------|
| Point | CircleMarker with fill, vary by category |
| LineString | Colored lines, vary weight by importance |
| Polygon | Semi-transparent fill with solid outline |

### 4.3 Output Formats

- PNG for web/documents (150-300 DPI)
- PDF for print quality
- SVG for scalable graphics

---

## Phase 5: Interactive Dashboard

### 5.1 Technology Stack

| Component | Recommended |
|-----------|-------------|
| Web framework | Flask (simple) or FastAPI (async) |
| Mapping library | Folium (Leaflet wrapper) |
| Basemaps | OpenStreetMap, ESRI, CartoDB |

### 5.2 Architecture Best Practices

- Separate map rendering from page template
- Use iframe or dedicated endpoint for map content
- Pre-load data on startup if dataset is static
- Cache expensive computations

### 5.3 Map Features to Include

- Multiple basemap options (street, satellite, ocean)
- Layer control with toggle visibility
- Feature popups with attribute details
- Tooltips on hover
- Fullscreen mode
- Measure tool for distances/areas
- Legend (positioned to not require scrolling)

### 5.4 Data Preparation for Web

- Convert all geometries to WGS84 (EPSG:4326)
- Convert datetime fields to strings (JSON serialization)
- Filter invalid/empty geometries
- Simplify geometries for large datasets
- Cluster dense point data

### 5.5 Performance Considerations

- Limit features displayed at once (< 10,000 for smooth interaction)
- Use marker clustering for dense point data
- Consider vector tiles for very large datasets
- Lazy-load layers that are initially hidden

---

## Best Practices Summary

### Error Handling

- Always wrap data loading in try/except blocks
- Log warnings for failed layers, don't crash
- Provide fallback values for missing data

### Coordinate Reference Systems

- Always check CRS before operations
- Transform to WGS84 for web mapping
- Use projected CRS for area/distance calculations

### Memory Management

- Load only required columns when possible
- Process large datasets in chunks
- Release memory after visualization is saved

### Documentation

- Document data sources and retrieval dates
- Record any transformations applied
- Note known data quality issues
- Include API endpoints and parameters used

### Reproducibility

- Save raw API responses
- Version control all scripts
- Document Python package versions
- Use relative paths in scripts

---

## Quick Reference

### Common CRS Codes

| EPSG | Name | Use Case |
|------|------|----------|
| 4326 | WGS84 | Web mapping, GPS |
| 28992 | Amersfoort / RD New | Netherlands |
| 32631 | UTM Zone 31N | North Sea |
| 3857 | Web Mercator | Web tiles |

### File Format Characteristics

| Format | Type | Multi-layer | Attributes |
|--------|------|-------------|------------|
| GDB | Vector | Yes | Full support |
| SHP | Vector | No | Limited (DBF) |
| GeoJSON | Vector | No | Full support |
| GeoPackage | Vector/Raster | Yes | Full support |
| GeoTIFF | Raster | No | Metadata only |

### Data Portal APIs

| Portal | Auth | Download Method |
|--------|------|-----------------|
| Pleio DataHub | None | Azure SAS tokens |
| AWS Open Data | None | S3 presigned URLs |
| Google Earth Engine | OAuth | GCS signed URLs |

---

## Pleio DataHub (Dutch Offshore Wind Data)

### Base URL

```
https://datahub.pleio.nl/api/v1/
```

### Endpoints

| Endpoint | Description |
|----------|-------------|
| `files/?limit=N&classification=ID` | List files by classification |
| `files/<ID>/` | Get file metadata |
| `files/<ID>/download/` | Get download URL with SAS token |
| `files/<ID>/?also_unpublished=true` | Include unpublished files |

### Classification IDs

| ID | Name | Description |
|----|------|-------------|
| 4 | GIS | Geographic Information System data |

### Example Request

```
https://datahub.pleio.nl/api/v1/files/?limit=25&classification=4
```

### Response Structure

```
{
  "count": N,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1234,
      "name": "filename.zip",
      "classification": {"id": 4, "name": "GIS"},
      "study": {"id": N, "name": "Study Type"},
      "zone": {"id": N, "name": "Zone Name"},
      "extension": {"id": N, "name": "ZIP"},
      "size": bytes,
      "nr_downloads": N,
      "published": true
    }
  ]
}
```

### Download URL Response

```
{
  "id": 1234,
  "download_command": "azcopy copy \"<URL>\" .",
  "download_url": "<URL_WITH_SAS_TOKEN>"
}
```

### Available Zones (Offshore Wind)

| Zone | Description |
|------|-------------|
| Hollandse Kust (noord) | Dutch coast north |
| Hollandse Kust (west) | Dutch coast west |
| Hollandse Kust (zuid) | Dutch coast south |
| IJmuiden Ver Alpha & Beta | IJmuiden far alpha/beta |
| IJmuiden Ver Gamma | IJmuiden far gamma |
| Nederwiek I | Nederwiek zone 1 |
| Doordewind | Doordewind zone |
| TNW | Ten noorden van de Waddeneilanden |

### Available Study Types

| Study | Description |
|-------|-------------|
| Geophysical data | Seismic, bathymetry, sonar surveys |
| Integrated Ground Model (IGM) | Combined geological/geotechnical model |
| Geological Groundmodel (GGM) | Geological subsurface model |
| Morphodynamics | Seabed dynamics and sediment transport |

### SAS Token Notes

- Tokens are valid for 7 days from generation
- Always fetch fresh URL immediately before download
- Use `azcopy` for large files (supports resume)

---

## Deliverables Checklist

- [ ] Raw data downloaded and archived
- [ ] Data inventory (JSON + Markdown)
- [ ] Static visualization (PNG)
- [ ] Interactive dashboard (Flask app)
- [ ] Process documentation (this file)
