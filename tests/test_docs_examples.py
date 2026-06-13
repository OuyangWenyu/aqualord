import json
import subprocess
import sys
from pathlib import Path


def test_mvp_doc_states_boundaries_and_links_examples():
    doc = Path("docs/mvp-v0.md").read_text(encoding="utf-8")

    assert "Opportunity Query" in doc
    assert "Asset Query" in doc
    assert "ADR 0001" in doc
    assert "aqualord opportunities" in doc
    assert "does not perform historical archive search" in doc
    assert "does not perform STAC Item/Asset querying" in doc
    assert "legacy knowledge sources" in doc


def test_sample_geojson_runs_through_cli():
    geo_path = Path("examples/query-region.geojson")
    assert geo_path.exists()

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
            "fixture",
            "--start",
            "2026-06-12T00:00:00Z",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    result = json.loads(completed.stdout)
    sample = json.loads(Path("examples/opportunity-result.json").read_text(encoding="utf-8"))

    assert result["command"] == sample["command"]
    assert result["opportunity_method"] == sample["opportunity_method"]
    assert len(result["opportunities"]) >= 1
