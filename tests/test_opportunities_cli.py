import json
import subprocess
import sys


def run_cli(tmp_path, geojson, *extra_args):
    geo_path = tmp_path / "query.geojson"
    geo_path.write_text(json.dumps(geojson), encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "aqualord",
            "opportunities",
            "--geo",
            str(geo_path),
            "--hours",
            "48",
            "--format",
            "json",
            *extra_args,
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(completed.stdout)


def test_point_geojson_returns_stable_empty_opportunity_result(tmp_path):
    result = run_cli(
        tmp_path,
        {
            "type": "Point",
            "coordinates": [114.3, 30.5],
        },
    )

    assert result["command"] == "opportunities"
    assert result["query_geometry"]["type"] == "Point"
    assert result["query_geometry"]["centroid"] == [114.3, 30.5]
    assert result["window"]["duration_hours"] == 48
    assert result["opportunities"] == []
    assert "warnings" in result
    assert "coverage" not in json.dumps(result).lower()


def test_polygon_geojson_returns_bbox_and_centroid_metadata(tmp_path):
    result = run_cli(
        tmp_path,
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [114.0, 30.0],
                    [115.0, 30.0],
                    [115.0, 31.0],
                    [114.0, 31.0],
                    [114.0, 30.0],
                ]
            ],
        },
    )

    assert result["query_geometry"]["type"] == "Polygon"
    assert result["query_geometry"]["bbox"] == [114.0, 30.0, 115.0, 31.0]
    assert result["query_geometry"]["centroid"] == [114.5, 30.5]
    assert result["opportunity_method"] == "centroid_pass_approx"


def test_default_result_includes_minimal_mission_catalog(tmp_path):
    result = run_cli(
        tmp_path,
        {
            "type": "Point",
            "coordinates": [114.3, 30.5],
        },
    )

    catalog = result["mission_catalog"]
    assert len(catalog) >= 5
    assert len(catalog) <= 30

    entry = catalog[0]
    for field in [
        "provider",
        "program",
        "mission",
        "constellation",
        "platform",
        "sensor",
        "products",
        "data_access",
    ]:
        assert field in entry

    assert "orbit" not in entry
    assert "tracking_ref" not in entry
    assert "sources" not in entry
    assert "source_notes" not in entry

    access = entry["data_access"][0]
    assert "kind" in access
    assert "href" in access
    assert set(access) <= {"kind", "href", "label"}


def test_fixture_orbit_provider_reports_tracking_and_staleness(tmp_path):
    result = run_cli(
        tmp_path,
        {
            "type": "Point",
            "coordinates": [114.3, 30.5],
        },
        "--orbit-provider",
        "fixture",
    )

    assert result["orbit_provider"] == "fixture"
    assert result["tracking_index"]["provider"] == "fixture"
    assert result["tracking_index"]["mapped_platforms"] >= 5
    assert "stale_orbit_records" in result["warnings"]
    assert "orbit" not in result["mission_catalog"][0]


def test_fixture_orbit_provider_returns_centroid_observation_opportunities(tmp_path):
    result = run_cli(
        tmp_path,
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [114.0, 30.0],
                    [115.0, 30.0],
                    [115.0, 31.0],
                    [114.0, 31.0],
                    [114.0, 30.0],
                ]
            ],
        },
        "--orbit-provider",
        "fixture",
        "--start",
        "2026-06-12T00:00:00Z",
    )

    opportunities = result["opportunities"]
    assert len(opportunities) >= 1
    first = opportunities[0]
    for field in [
        "provider",
        "program",
        "mission",
        "constellation",
        "platform",
        "sensor",
        "possible_products",
        "data_access",
        "pass_start",
        "pass_end",
        "peak_time",
        "confidence",
        "opportunity_method",
        "warnings",
    ]:
        assert field in first

    assert first["opportunity_method"] == "centroid_pass_approx"
    assert "does_not_confirm_acquisition" in first["warnings"]
    assert "does_not_confirm_product_availability" in first["warnings"]
    assert "stac_item" not in json.dumps(first).lower()
    assert "coverage" not in json.dumps(first).lower()


def test_celestrak_provider_can_use_prefilled_cache_from_cli(tmp_path):
    geo_path = tmp_path / "query.geojson"
    geo_path.write_text(
        json.dumps({"type": "Point", "coordinates": [114.3, 30.5]}),
        encoding="utf-8",
    )
    cache_root = tmp_path / "cache" / "celestrak"
    cache_root.mkdir(parents=True)
    for catalog_number in ["40697", "42063", "39084", "49260", "43013", "40376"]:
        (cache_root / f"{catalog_number}.tle").write_text(
            f"PLATFORM {catalog_number}\n1 {catalog_number}U\n2 {catalog_number}\n",
            encoding="utf-8",
        )
        (cache_root / f"{catalog_number}.meta.json").write_text(
            '{"fetched_at": "2026-06-12T00:00:00Z"}',
            encoding="utf-8",
        )

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "aqualord",
            "opportunities",
            "--geo",
            str(geo_path),
            "--hours",
            "48",
            "--format",
            "json",
            "--orbit-provider",
            "celestrak",
            "--cache-dir",
            str(tmp_path / "cache"),
            "--start",
            "2026-06-12T00:00:00Z",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    result = json.loads(completed.stdout)
    assert result["orbit_provider"] == "celestrak"
    assert result["tracking_index"]["provider"] == "celestrak"
    assert "served_from_cache" in result["warnings"]
