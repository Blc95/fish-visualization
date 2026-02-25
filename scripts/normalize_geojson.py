import json
import unicodedata
from pathlib import Path


def normalize_zone(value: object) -> str:
    """Normalize zone names to improve matching with cleaned CSV values."""
    if value is None:
        return ""
    return unicodedata.normalize("NFKC", str(value)).strip().casefold()


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    in_path = repo_root / "data" / "raw" / "creeks.geojson"
    out_path = repo_root / "data" / "processed" / "normalized_creeks.geojson"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8") as f:
        geojson = json.load(f)

    for feature in geojson.get("features", []):
        props = feature.get("properties", {})
        if "Zone" in props:
            props["Zone"] = normalize_zone(props["Zone"])

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False)

    print(f"Wrote normalized GeoJSON to: {out_path}")


if __name__ == "__main__":
    main()