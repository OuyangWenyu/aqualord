from datetime import datetime, timedelta, timezone

from aqualord.celestrak import load_celestrak_orbits


def test_fetches_and_caches_raw_tle_records(tmp_path):
    calls = []

    def fetcher(url):
        calls.append(url)
        return "SENTINEL-2A\n1 40697U 15028A\n2 40697\n"

    tracking_index = [
        {
            "platform_id": "sentinel-2a",
            "provider": "celestrak",
            "provider_lookup_id": "40697",
        }
    ]

    records, warnings = load_celestrak_orbits(
        tracking_index,
        tmp_path,
        fetcher=fetcher,
        now=datetime(2026, 6, 12, tzinfo=timezone.utc),
    )

    assert len(calls) == 1
    assert "CATNR=40697" in calls[0]
    assert "FORMAT=TLE" in calls[0]
    assert records[0]["platform_id"] == "sentinel-2a"
    assert records[0]["raw"] == "SENTINEL-2A\n1 40697U 15028A\n2 40697\n"
    assert "missing_orbit_records" not in warnings

    cached_records, cached_warnings = load_celestrak_orbits(
        tracking_index,
        tmp_path,
        fetcher=fetcher,
        now=datetime(2026, 6, 12, 1, tzinfo=timezone.utc),
    )

    assert len(calls) == 1
    assert cached_records[0]["raw"] == records[0]["raw"]
    assert "served_from_cache" in cached_warnings


def test_uses_stale_cache_when_refresh_fails(tmp_path):
    def failing_fetcher(url):
        raise RuntimeError("network unavailable")

    tracking_index = [
        {
            "platform_id": "sentinel-2a",
            "provider": "celestrak",
            "provider_lookup_id": "40697",
        }
    ]

    stale_time = datetime(2026, 6, 1, tzinfo=timezone.utc)
    record_dir = tmp_path / "celestrak"
    record_dir.mkdir()
    (record_dir / "40697.tle").write_text("STALE TLE\n", encoding="utf-8")
    (record_dir / "40697.meta.json").write_text(
        '{"fetched_at": "' + stale_time.isoformat().replace("+00:00", "Z") + '"}',
        encoding="utf-8",
    )

    records, warnings = load_celestrak_orbits(
        tracking_index,
        tmp_path,
        fetcher=failing_fetcher,
        now=stale_time + timedelta(days=30),
    )

    assert records[0]["raw"] == "STALE TLE\n"
    assert "stale_orbit_records" in warnings
    assert "served_from_cache" in warnings
