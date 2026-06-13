from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from .catalog import load_default_catalog
from .celestrak import load_celestrak_orbits
from .geojson import load_query_geojson
from .orbits import load_fixture_orbits, orbit_warnings
from .tracking import load_default_tracking_index, tracking_summary


def build_empty_result(
    geojson_path: str,
    hours: int,
    orbit_provider: str = "none",
    start: str | None = None,
    cache_dir: str | None = None,
) -> dict:
    if hours <= 0:
        raise ValueError("--hours must be greater than zero.")

    start_time = _parse_start(start) if start else datetime.now(timezone.utc).replace(microsecond=0)
    end_time = start_time + timedelta(hours=hours)
    query_geometry = load_query_geojson(geojson_path)

    catalog = load_default_catalog()
    warnings = [
        "does_not_confirm_acquisition",
        "does_not_confirm_product_availability",
    ]
    result = {
        "command": "opportunities",
        "query_geometry": query_geometry,
        "window": {
            "start": start_time.isoformat().replace("+00:00", "Z"),
            "end": end_time.isoformat().replace("+00:00", "Z"),
            "duration_hours": hours,
        },
        "opportunity_method": "centroid_pass_approx",
        "mission_catalog": catalog,
        "orbit_provider": orbit_provider,
        "opportunities": [],
        "warnings": warnings,
    }

    if orbit_provider == "fixture":
        tracking_index = load_default_tracking_index()
        orbit_records = load_fixture_orbits()
        result["tracking_index"] = tracking_summary(tracking_index, "fixture")
        result["opportunities"] = _opportunities_from_fixture_records(
            catalog,
            orbit_records,
            start_time,
            end_time,
        )
        result["warnings"].extend(orbit_warnings(orbit_records, tracking_index))
    elif orbit_provider == "celestrak":
        tracking_index = load_default_tracking_index()
        orbit_records, provider_warnings = load_celestrak_orbits(
            tracking_index,
            Path(cache_dir or ".aqualord-cache"),
            now=start_time,
        )
        result["tracking_index"] = tracking_summary(tracking_index, "celestrak")
        result["orbit_records"] = [
            {
                "platform_id": record["platform_id"],
                "provider": record["provider"],
                "provider_lookup_id": record["provider_lookup_id"],
                "fetched_at": record["fetched_at"],
            }
            for record in orbit_records
        ]
        result["warnings"].extend(provider_warnings)
    else:
        result["warnings"].append("no_orbit_provider_loaded")

    return result


def _parse_start(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _opportunities_from_fixture_records(
    catalog: list[dict[str, Any]],
    orbit_records: list[dict[str, Any]],
    start: datetime,
    end: datetime,
) -> list[dict[str, Any]]:
    catalog_by_id = {entry["id"]: entry for entry in catalog}
    opportunities: list[dict[str, Any]] = []

    for record in orbit_records:
        catalog_entry = catalog_by_id.get(record.get("platform_id"))
        if not catalog_entry:
            continue
        for pass_window in record.get("pass_windows", []):
            pass_start = _parse_start(pass_window["pass_start"])
            pass_end = _parse_start(pass_window["pass_end"])
            if pass_end < start or pass_start > end:
                continue
            opportunities.append(_build_opportunity(catalog_entry, pass_window))

    return opportunities


def _build_opportunity(catalog_entry: dict[str, Any], pass_window: dict[str, str]) -> dict[str, Any]:
    sensor = catalog_entry["sensor"]
    return {
        "provider": catalog_entry["provider"],
        "program": catalog_entry["program"],
        "mission": catalog_entry["mission"],
        "constellation": catalog_entry["constellation"],
        "platform": catalog_entry["platform"],
        "sensor": sensor,
        "possible_products": catalog_entry["products"],
        "data_access": catalog_entry["data_access"],
        "resolution": sensor["resolution"],
        "swath_km": sensor["swath_km"],
        "pass_start": pass_window["pass_start"],
        "pass_end": pass_window["pass_end"],
        "peak_time": pass_window["peak_time"],
        "confidence": "medium",
        "opportunity_method": "centroid_pass_approx",
        "warnings": [
            "theoretical_opportunity",
            "does_not_confirm_acquisition",
            "does_not_confirm_cloud_free_observation",
            "does_not_confirm_downlink",
            "does_not_confirm_processing",
            "does_not_confirm_publication",
            "does_not_confirm_product_availability",
        ],
    }
