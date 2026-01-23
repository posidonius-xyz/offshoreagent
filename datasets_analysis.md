# Summary of Available GIS Datasets for Geographic Analysis

The API returned **16 GIS datasets** from the Dutch offshore wind data hub (Pleio). All datasets are classified as **GIS** and relate to **Soil** chapter data.

## By Study Type

| Study Type | Count | Description |
|------------|-------|-------------|
| Geophysical data | 8 | Seabed and subsurface survey data |
| Integrated Ground Model (IGM) | 5 | Combined geological/geotechnical models |
| Geological Groundmodel (GGM) | 2 | Geological subsurface models |
| Morphodynamics | 1 | Seabed dynamics and sediment transport |

## By Geographic Zone

| Zone | Datasets | Total Size |
|------|----------|------------|
| IJmuiden Ver Alpha & Beta | 4 | ~41.5 GB |
| Hollandse Kust (noord) | 3 | ~36.4 GB |
| Hollandse Kust (zuid) | 2 | ~24.1 GB |
| Hollandse Kust (west) | 1 | ~54.3 GB |
| Nederwiek I (Zuid) | 2 | ~70.1 GB |
| IJmuiden Ver Gamma | 1 | ~40.8 GB |
| Doordewind | 1 | ~46.9 GB |
| TNW | 2 | ~21.1 GB |

## File Formats

- **ZIP**: 9 datasets
- **RAR**: 5 datasets
- **7Z**: 1 dataset
- **MPK** (ArcGIS Map Package): 1 dataset

## Most Downloaded Datasets

1. **HWK_GP– GIS.rar** - 585 downloads (Hollandse Kust west, Geophysical)
2. **IJV_IGM_GIS.zip** - 397 downloads (IJmuiden Ver, Integrated Ground Model)
3. **IJV- Morphodynamics – GIS.rar** - 259 downloads

## Key Observations

- All datasets focus on **Dutch North Sea offshore wind farm zones**
- Data spans from 2023 to 2025
- Total combined size: **~335 GB** of GIS data
- Most data relates to geophysical surveys and ground modeling for wind farm foundation design
- The most popular datasets are for the Hollandse Kust and IJmuiden Ver wind farm areas

## Data Source

- **API Endpoint**: `https://datahub.pleio.nl/api/v1/files/?limit=25&classification=4`
- **Classification**: GIS (ID: 4)
- **Retrieved**: 16 records
