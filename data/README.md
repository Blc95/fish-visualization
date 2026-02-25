# Data

## Raw
- `raw/fish.csv`: Catch records dataset (source file used by the app).
- `raw/creeks.geojson`: Creek geometries with zone names.

## Processed
- `processed/normalized_creeks.geojson`: GeoJSON where `properties.Zone` has been normalized (unicode normalization + whitespace + casefold) to match cleaned zone values in the dataset.

To regenerate processed files, run:
- `python3 scripts/normalize_geojson.py`

