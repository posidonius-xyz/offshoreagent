"""
GDB File Inventory Script
Explores ESRI File Geodatabase and creates a data inventory
"""

import fiona
from pathlib import Path
import json

gdb_path = "./data-extracted/RVO_NW_I_GGM.gdb"

print("=" * 70)
print("GIS DATA INVENTORY - Nederwiek I Geological Ground Model")
print("=" * 70)
print(f"\nGeodatabase: {gdb_path}\n")

# List all layers in the geodatabase
layers = fiona.listlayers(gdb_path)
print(f"Total layers found: {len(layers)}\n")

vector_layers = []
failed_layers = []

print("-" * 70)
print("LAYER DETAILS")
print("-" * 70)

for layer_name in sorted(layers):
    try:
        with fiona.open(gdb_path, layer=layer_name) as src:
            geom_type = src.schema.get('geometry', 'None')
            crs = str(src.crs) if src.crs else 'Unknown'
            feature_count = len(src)
            properties = list(src.schema['properties'].keys())
            bounds = src.bounds if feature_count > 0 else None

            layer_info = {
                'name': layer_name,
                'geometry_type': geom_type,
                'crs': crs,
                'feature_count': feature_count,
                'fields': properties,
                'bounds': bounds
            }
            vector_layers.append(layer_info)

            print(f"\n{layer_name}")
            print(f"  Type: {geom_type or 'Table'} | Features: {feature_count} | Fields: {len(properties)}")
            if properties:
                print(f"  Fields: {', '.join(properties[:5])}{'...' if len(properties) > 5 else ''}")

    except Exception as e:
        failed_layers.append({'name': layer_name, 'error': str(e)})
        print(f"\n{layer_name}")
        print(f"  [Could not open - likely raster or system table]")

# Group by geometry type
print("\n" + "=" * 70)
print("SUMMARY BY GEOMETRY TYPE")
print("=" * 70)

by_geom = {}
for layer in vector_layers:
    geom = layer['geometry_type'] or 'Table'
    if geom not in by_geom:
        by_geom[geom] = []
    by_geom[geom].append(layer)

for geom_type, layers_list in sorted(by_geom.items()):
    layer_names = [l['name'] for l in layers_list]
    total_features = sum(l['feature_count'] for l in layers_list)
    print(f"\n{geom_type}: {len(layers_list)} layers, {total_features:,} features")
    for name in layer_names[:10]:
        print(f"  - {name}")
    if len(layer_names) > 10:
        print(f"  ... and {len(layer_names) - 10} more")

# Overall summary
print("\n" + "=" * 70)
print("OVERALL SUMMARY")
print("=" * 70)
print(f"Total layers listed: {len(layers)}")
print(f"Vector layers loaded: {len(vector_layers)}")
print(f"Raster/other layers: {len(failed_layers)}")
total_features = sum(l['feature_count'] for l in vector_layers)
print(f"Total features: {total_features:,}")

# Export to JSON
inventory = {
    'geodatabase': gdb_path,
    'total_layers': len(layers),
    'vector_layers_count': len(vector_layers),
    'raster_layers_count': len(failed_layers),
    'total_features': total_features,
    'vector_layers': vector_layers,
    'raster_layers': [l['name'] for l in failed_layers]
}

with open('gdb_inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)

print(f"\nDetailed inventory saved to: gdb_inventory.json")
