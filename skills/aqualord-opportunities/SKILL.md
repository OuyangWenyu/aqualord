---
name: aqualord-opportunities
description: Use Aqualord's installed CLI to query future or near-real-time remote-sensing Observation Opportunities for a user-provided region. Trigger when the user asks what satellite/remote-sensing data may observe a place, city, basin, bbox, point, polygon, or GeoJSON in an upcoming time window; when they ask Codex to run `aqualord opportunities`; or when they want a concise interpretation of Aqualord opportunity JSON.
---

# Aqualord Opportunities

Use the CLI as the source of truth. Do not reimplement catalog lookup, GeoJSON parsing, orbit retrieval, or opportunity filtering inside the skill.

## Workflow

1. Confirm `aqualord` is installed with `aqualord --help`.
2. If the user supplied GeoJSON, use it directly. If they supplied a place, bbox, point, basin, or rough area, create a temporary GeoJSON file.
3. Run the base command when the user only needs catalog/query-shape validation:

```bash
aqualord opportunities --geo <query.geojson> --hours <hours> --format json
```

The base command currently uses `orbit_provider=none`, so it can return zero opportunities even when relevant satellites exist. Do not interpret that as "no observation opportunities"; interpret it as "no orbit provider was loaded."

For deterministic opportunity demos, add:

```bash
--orbit-provider fixture --start 2026-06-12T00:00:00Z
```

4. Parse the JSON and summarize `platform`, `sensor`, `possible_products`, `pass_start`, `pass_end`, `confidence`, and `data_access`.
5. Preserve caveats. An Observation Opportunity is theoretical and does not confirm acquisition, cloud-free observation, downlink, processing, publication, or product availability.

## GeoJSON

Use WGS84 longitude/latitude coordinates. For a rough bbox:

```json
{
  "type": "Polygon",
  "coordinates": [[
    [min_lon, min_lat],
    [max_lon, min_lat],
    [max_lon, max_lat],
    [min_lon, max_lat],
    [min_lon, min_lat]
  ]]
}
```

## Installation Fallback

If `aqualord` is not found and the local repo is available, install the editable CLI:

```bash
uv tool install --editable D:\Code\aqualord --force
```

Then rerun `aqualord --help`. If the install location is not on `PATH`, use:

```bash
uv run --project D:\Code\aqualord aqualord opportunities --geo <query.geojson> --hours <hours> --format json
```

## Boundaries

Do not present fixture output as live prediction. The fixture provider only verifies the CLI/output workflow. Real future opportunity results require a real orbit propagation provider.

Do not treat an empty result from `orbit_provider=none` as evidence that no satellite can observe the region.

Do not call historical STAC assets an Observation Opportunity. Historical archive search belongs to a separate Asset Query path.
