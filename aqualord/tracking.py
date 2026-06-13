import json
from importlib import resources
from typing import Any


REQUIRED_TRACKING_FIELDS = {"platform_id", "provider", "provider_lookup_id"}


def load_default_tracking_index() -> list[dict[str, str]]:
    with resources.files("aqualord.data").joinpath("tracking_index.json").open(
        "r", encoding="utf-8"
    ) as handle:
        return validate_tracking_index(json.load(handle))


def validate_tracking_index(entries: Any) -> list[dict[str, str]]:
    if not isinstance(entries, list):
        raise ValueError("Tracking Index must be a list.")

    seen = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Tracking Index entries must be objects.")
        missing = REQUIRED_TRACKING_FIELDS - set(entry)
        if missing:
            raise ValueError(f"Tracking Index entry is missing fields: {sorted(missing)}")
        platform_id = entry["platform_id"]
        if platform_id in seen:
            raise ValueError(f"Duplicate Tracking Index platform_id: {platform_id}")
        seen.add(platform_id)

    return entries


def tracking_summary(entries: list[dict[str, str]], provider: str) -> dict:
    return {
        "provider": provider,
        "mapped_platforms": len(entries),
    }
