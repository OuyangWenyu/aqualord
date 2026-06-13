import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
from urllib.parse import urlencode
from urllib.request import urlopen


CELESTRAK_GP_URL = "https://celestrak.org/NORAD/elements/gp.php"
DEFAULT_MAX_AGE_HOURS = 24


def load_celestrak_orbits(
    tracking_index: list[dict],
    cache_dir: Path,
    *,
    fetcher: Callable[[str], str] | None = None,
    now: datetime | None = None,
    max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
) -> tuple[list[dict], list[str]]:
    fetcher = fetcher or _fetch_text
    now = now or datetime.now(timezone.utc)
    cache_root = cache_dir / "celestrak"
    cache_root.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    warnings: list[str] = []

    for entry in tracking_index:
        if entry.get("provider") != "celestrak":
            continue

        lookup_id = str(entry["provider_lookup_id"])
        tle_path = cache_root / f"{lookup_id}.tle"
        meta_path = cache_root / f"{lookup_id}.meta.json"
        cached_at = _read_cached_at(meta_path)

        if tle_path.exists() and cached_at and _is_fresh(cached_at, now, max_age_hours):
            records.append(_record_from_cache(entry, tle_path, cached_at))
            _add_warning(warnings, "served_from_cache")
            continue

        try:
            raw = fetcher(_celestrak_tle_url(lookup_id))
            if not raw.strip():
                raise ValueError("CelesTrak returned an empty response.")
            tle_path.write_text(raw, encoding="utf-8")
            meta_path.write_text(
                json.dumps({"fetched_at": _format_time(now)}, indent=2),
                encoding="utf-8",
            )
            records.append(
                {
                    "platform_id": entry["platform_id"],
                    "provider": "celestrak",
                    "provider_lookup_id": lookup_id,
                    "fetched_at": _format_time(now),
                    "raw": raw,
                }
            )
        except Exception:
            if tle_path.exists():
                records.append(_record_from_cache(entry, tle_path, cached_at))
                _add_warning(warnings, "served_from_cache")
                _add_warning(warnings, "stale_orbit_records")
            else:
                _add_warning(warnings, "missing_orbit_records")

    if not records:
        _add_warning(warnings, "missing_orbit_records")

    return records, warnings


def _celestrak_tle_url(catalog_number: str) -> str:
    return f"{CELESTRAK_GP_URL}?{urlencode({'CATNR': catalog_number, 'FORMAT': 'TLE'})}"


def _fetch_text(url: str) -> str:
    with urlopen(url, timeout=20) as response:
        return response.read().decode("utf-8")


def _record_from_cache(entry: dict, tle_path: Path, cached_at: datetime | None) -> dict:
    return {
        "platform_id": entry["platform_id"],
        "provider": "celestrak",
        "provider_lookup_id": str(entry["provider_lookup_id"]),
        "fetched_at": _format_time(cached_at) if cached_at else None,
        "raw": tle_path.read_text(encoding="utf-8"),
    }


def _read_cached_at(meta_path: Path) -> datetime | None:
    if not meta_path.exists():
        return None
    metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    fetched_at = metadata.get("fetched_at")
    if not fetched_at:
        return None
    return datetime.fromisoformat(fetched_at.replace("Z", "+00:00")).astimezone(timezone.utc)


def _is_fresh(cached_at: datetime, now: datetime, max_age_hours: int) -> bool:
    return (now - cached_at).total_seconds() <= max_age_hours * 3600


def _format_time(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _add_warning(warnings: list[str], warning: str) -> None:
    if warning not in warnings:
        warnings.append(warning)
