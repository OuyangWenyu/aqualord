# Aqualord MVP v0

Aqualord MVP v0 is an Opportunity Query engine for user-provided Query GeoJSON. It estimates future or near-real-time Observation Opportunities and connects them to possible products and minimal Data Access entry points.

It is not an Asset Query engine. It does not perform historical archive search, and it does not perform STAC Item/Asset querying.

## Command

```bash
python -m aqualord opportunities --geo examples/query-region.geojson --hours 48 --format json --orbit-provider fixture --start 2026-06-12T00:00:00Z
```

Installed environments can expose the same command as:

```bash
aqualord opportunities --geo examples/query-region.geojson --hours 48 --format json
```

## CLI Installation

For a GitHub CLI-like local development experience, install the package as a global uv tool:

```bash
uv tool install --editable D:\Code\aqualord --force
```

After installation, `aqualord` can be called from any working directory:

```bash
aqualord opportunities --geo path/to/query.geojson --hours 48 --format json
```

Codex should prefer the installed CLI over reading or reimplementing package internals. If the global command is unavailable, use `uv run --project D:\Code\aqualord aqualord ...` as a fallback.

## Codex Skill

The repository includes a thin Codex skill at `skills/aqualord-opportunities`. Its role is to route natural-language opportunity questions into the installed CLI, prepare GeoJSON input when needed, and summarize JSON output with the correct caveats.

Install the skill for Codex discovery by linking or copying it to:

```text
C:\Users\owen\.codex\skills\aqualord-opportunities
```

## What v0 Returns

The JSON output is an `OpportunityResult` with:

- query geometry metadata
- query window
- `opportunity_method: centroid_pass_approx`
- Mission Catalog metadata for provider, program, mission, constellation, platform, sensor, products, and Data Access
- theoretical pass windows when an orbit provider can supply them
- warnings and caveats that prevent treating opportunities as confirmed assets

See `examples/opportunity-result.json` for a runnable sample output shape.

## Boundaries

MVP v0 does not perform historical archive search.
MVP v0 does not perform STAC Item/Asset querying.
MVP v0 does not perform cloud screening.
MVP v0 does not confirm acquisition, downlink, processing, publication, or product availability.
MVP v0 does not perform basin-id lookup or hydrologic topology analysis.

Predicted opportunities are not STAC Items. ADR 0001 records this decision: `docs/adr/0001-separate-observation-opportunities-from-stac-assets.md`.

## Legacy Knowledge Sources

Existing folders such as `Landsat/`, `MODIS/`, `SMAP/`, `CAMELS/`, `GAGES/`, `HydroSHEDS/`, and `NH/` remain legacy knowledge sources. MVP v0 builds the new package alongside these notes rather than moving or reorganizing them.

## Future Asset Query Path

Historical and archived products should be added later as an Asset Query path using STAC APIs, Collections, Items, Assets, and Links where possible. Aqualord should not invent a replacement historical asset schema.
