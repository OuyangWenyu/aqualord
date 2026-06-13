import json
from datetime import datetime, timezone
from importlib import resources
from typing import Any


STALE_AFTER_DAYS = 14


def load_fixture_orbits() -> list[dict[str, Any]]:
    with resources.files("aqualord.data").joinpath("fixture_orbits.json").open(
        "r", encoding="utf-8"
    ) as handle:
        records = json.load(handle)
    if not isinstance(records, list):
        raise ValueError("Fixture orbit records must be a list.")
    return records


def orbit_warnings(records: list[dict[str, Any]], tracking_index: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    tracked_platforms = {entry["platform_id"] for entry in tracking_index}
    orbit_platforms = {record.get("platform_id") for record in records}

    if tracked_platforms - orbit_platforms:
        warnings.append("missing_orbit_records")

    if any(_is_stale(record) for record in records):
        warnings.append("stale_orbit_records")

    return warnings


def _is_stale(record: dict[str, Any]) -> bool:
    fetched_at = record.get("fetched_at")
    if not fetched_at:
        return True
    fetched = datetime.fromisoformat(fetched_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return (now - fetched).days > STALE_AFTER_DAYS
