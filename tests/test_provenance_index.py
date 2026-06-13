from aqualord.catalog import load_default_catalog
from aqualord.provenance import load_default_provenance_index, provenance_for


def test_default_provenance_index_links_catalog_fields_to_sources():
    catalog = load_default_catalog()
    provenance = load_default_provenance_index(catalog)

    entry = provenance_for(provenance, "sentinel-2a", "sensor.swath_km")

    assert entry["catalog_entry_id"] == "sentinel-2a"
    assert entry["field_path"] == "sensor.swath_km"
    assert "source_name" in entry
    assert "source_url" in entry
    assert "retrieved_at" in entry
    assert entry["confidence"] in {"low", "medium", "high"}


def test_required_catalog_fields_have_provenance():
    catalog = load_default_catalog()
    provenance = load_default_provenance_index(catalog)
    indexed = {
        (entry["catalog_entry_id"], entry["field_path"])
        for entry in provenance
    }

    for catalog_entry in catalog:
        for field_path in ["sensor.resolution", "sensor.swath_km", "data_access"]:
            assert (catalog_entry["id"], field_path) in indexed
