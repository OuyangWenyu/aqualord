import io
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))

import generate_frontend_catalog as gen  # noqa: E402


class TestParseResolutionM:
    def test_single_value_meters(self):
        assert gen.parse_resolution_m("300 m") == 300

    def test_multi_value_extracts_first(self):
        assert gen.parse_resolution_m("10/20/60 m") == 10

    def test_kilometers_converts_to_meters(self):
        assert gen.parse_resolution_m("9/36 km") == 9000

    def test_single_kilometer(self):
        assert gen.parse_resolution_m("1 km") == 1000

    def test_raises_on_unparseable(self):
        with pytest.raises(ValueError):
            gen.parse_resolution_m("no numbers here")


class TestGenerate:
    def test_unknown_modality_raises(self, tmp_path):
        catalog = tmp_path / "catalog.json"
        tracking = tmp_path / "tracking.json"
        output = tmp_path / "out.json"

        catalog.write_text(
            json.dumps([
                {
                    "id": "test-plat",
                    "provider": "NASA",
                    "platform": "Test Platform",
                    "sensor": {
                        "name": "TEST-SENSOR",
                        "modality": "impossible_hyperspectral_lidar",
                        "resolution": "10 m",
                        "swath_km": 100,
                    },
                }
            ]),
            encoding="utf-8",
        )
        tracking.write_text(
            json.dumps([
                {
                    "platform_id": "test-plat",
                    "provider": "celestrak",
                    "provider_lookup_id": "99999",
                }
            ]),
            encoding="utf-8",
        )

        gen.CATALOG_PATH = catalog
        gen.TRACKING_PATH = tracking
        gen.OUTPUT_PATH = output

        with pytest.raises(ValueError, match="impossible_hyperspectral_lidar"):
            gen.generate()

    def test_missing_tracking_warns(self, tmp_path):
        catalog = tmp_path / "catalog.json"
        tracking = tmp_path / "tracking.json"
        output = tmp_path / "out.json"

        catalog.write_text(
            json.dumps([
                {
                    "id": "orphan-plat",
                    "provider": "ESA",
                    "platform": "Orphan",
                    "sensor": {
                        "name": "SAR",
                        "modality": "sar",
                        "resolution": "5 m",
                        "swath_km": 200,
                    },
                }
            ]),
            encoding="utf-8",
        )
        tracking.write_text(json.dumps([]), encoding="utf-8")

        gen.CATALOG_PATH = catalog
        gen.TRACKING_PATH = tracking
        gen.OUTPUT_PATH = output

        old_stderr = sys.stderr
        sys.stderr = io.StringIO()
        try:
            gen.generate()
        finally:
            stderr_output = sys.stderr.getvalue()
            sys.stderr = old_stderr

        assert "orphan-plat" in stderr_output
        assert "no tracking entry" in stderr_output
        assert json.loads(output.read_text(encoding="utf-8")) == []
