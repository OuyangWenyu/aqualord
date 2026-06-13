import json
from importlib import resources
from typing import Any


REQUIRED_FIELDS = {
    "id",
    "provider",
    "program",
    "mission",
    "constellation",
    "platform",
    "sensor",
    "products",
    "data_access",
}

FORBIDDEN_CATALOG_FIELDS = {"orbit", "tracking_ref", "sources", "source_notes"}


def load_default_catalog() -> list[dict[str, Any]]:
    with resources.files("aqualord.data").joinpath("mission_catalog.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return validate_catalog(json.load(handle))


def validate_catalog(entries: Any) -> list[dict[str, Any]]:
    if not isinstance(entries, list):
        raise ValueError("Mission Catalog must be a list.")
    if not 5 <= len(entries) <= 10:
        raise ValueError("MVP v0 Mission Catalog must contain 5-10 platform entries.")

    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Mission Catalog entries must be objects.")
        missing = REQUIRED_FIELDS - set(entry)
        if missing:
            raise ValueError(f"Mission Catalog entry is missing fields: {sorted(missing)}")
        forbidden = FORBIDDEN_CATALOG_FIELDS & set(entry)
        if forbidden:
            raise ValueError(f"Mission Catalog entry embeds non-catalog fields: {sorted(forbidden)}")
        _validate_data_access(entry["data_access"])

    return entries


def _validate_data_access(access_entries: Any) -> None:
    if not isinstance(access_entries, list) or not access_entries:
        raise ValueError("data_access must be a non-empty list.")

    for access in access_entries:
        if not isinstance(access, dict):
            raise ValueError("data_access entries must be objects.")
        missing = {"kind", "href"} - set(access)
        if missing:
            raise ValueError(f"data_access entry is missing fields: {sorted(missing)}")
        extra = set(access) - {"kind", "href", "label"}
        if extra:
            raise ValueError(f"data_access entry has non-v0 fields: {sorted(extra)}")
