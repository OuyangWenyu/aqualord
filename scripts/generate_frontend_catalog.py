"""Generate curatedSatellites.generated.json from Python catalog + tracking index.

Reads mission_catalog.json and tracking_index.json, transforms entries to the
TypeScript SatelliteConfig shape, and writes the JSON artifact used by the
frontend.
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CATALOG_PATH = PROJECT_ROOT / "aqualord" / "data" / "mission_catalog.json"
TRACKING_PATH = PROJECT_ROOT / "aqualord" / "data" / "tracking_index.json"
OUTPUT_PATH = (
    PROJECT_ROOT
    / "src"
    / "domain"
    / "satellites"
    / "curatedSatellites.generated.json"
)

SENSOR_TYPE_MAP: dict[str, str] = {
    "multispectral_optical": "multispectral",
    "multispectral_thermal": "multispectral",
    "sar": "sar",
    "multispectral_optical_thermal": "weather",
    "passive_microwave": "multispectral",
}

OPERATOR_MAP: dict[str, str] = {
    "USGS": "NASA/USGS",
}


def parse_resolution_m(resolution: str) -> int:
    match = re.search(r"(\d+)", resolution)
    if not match:
        raise ValueError(f"Cannot parse resolution: {resolution!r}")
    value = int(match.group(1))
    if "km" in resolution.lower():
        value *= 1000
    return value


def generate() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    tracking_entries = json.loads(TRACKING_PATH.read_text(encoding="utf-8"))

    tracking_by_id: dict[str, str] = {
        t["platform_id"]: t["provider_lookup_id"] for t in tracking_entries
    }

    result: list[dict] = []
    for entry in catalog:
        platform_id = entry["id"]
        norad_str = tracking_by_id.get(platform_id)
        if norad_str is None:
            print(
                f"Warning: {platform_id!r} has no tracking entry, skipping",
                file=sys.stderr,
            )
            continue

        sensor = entry["sensor"]
        modality = sensor["modality"]
        if modality not in SENSOR_TYPE_MAP:
            raise ValueError(
                f"Unknown sensor modality {modality!r} for {entry['id']}; "
                f"add it to SENSOR_TYPE_MAP"
            )
        result.append(
            {
                "noradId": int(norad_str),
                "name": entry["platform"],
                "operator": OPERATOR_MAP.get(entry["provider"], entry["provider"]),
                "sensorType": SENSOR_TYPE_MAP[modality],
                "swathKm": sensor["swath_km"],
                "resolutionM": parse_resolution_m(sensor["resolution"]),
                "source": f"{entry['provider']} {sensor['name']} public mission specifications",
            }
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"Wrote {len(result)} satellites to {OUTPUT_PATH}")


if __name__ == "__main__":
    generate()
