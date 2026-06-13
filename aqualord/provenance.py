import json
from importlib import resources
from typing import Any


REQUIRED_PROVENANCE_FIELDS = {
    "catalog_entry_id",
    "field_path",
    "source_name",
    "source_url",
    "retrieved_at",
    "confidence",
}

REQUIRED_CATALOG_PROVENANCE_PATHS = {
    "sensor.resolution",
    "sensor.swath_km",
    "data_access",
}


def load_default_provenance_index(catalog: list[dict[str, Any]] | None = None) -> list[dict[str, str]]:
    with resources.files("aqualord.data").joinpath("provenance_index.json").open(
        "r", encoding="utf-8"
    ) as handle:
        entries = validate_provenance_index(json.load(handle))

    if catalog is not None:
        validate_catalog_provenance(catalog, entries)

    return entries


def validate_provenance_index(entries: Any) -> list[dict[str, str]]:
    if not isinstance(entries, list):
        raise ValueError("Provenance Index must be a list.")

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Provenance Index entries must be objects.")
        missing = REQUIRED_PROVENANCE_FIELDS - set(entry)
        if missing:
            raise ValueError(f"Provenance Index entry is missing fields: {sorted(missing)}")
        if entry["confidence"] not in {"low", "medium", "high"}:
            raise ValueError(f"Invalid provenance confidence: {entry['confidence']}")

    return entries


def validate_catalog_provenance(
    catalog: list[dict[str, Any]],
    provenance: list[dict[str, str]],
) -> None:
    indexed = {
        (entry["catalog_entry_id"], entry["field_path"])
        for entry in provenance
    }
    missing = []
    for catalog_entry in catalog:
        entry_id = catalog_entry["id"]
        for field_path in REQUIRED_CATALOG_PROVENANCE_PATHS:
            if (entry_id, field_path) not in indexed:
                missing.append(f"{entry_id}:{field_path}")
    if missing:
        raise ValueError(f"Missing required provenance: {missing}")


def provenance_for(
    provenance: list[dict[str, str]],
    catalog_entry_id: str,
    field_path: str,
) -> dict[str, str]:
    for entry in provenance:
        if entry["catalog_entry_id"] == catalog_entry_id and entry["field_path"] == field_path:
            return entry
    raise KeyError(f"No provenance for {catalog_entry_id}:{field_path}")
