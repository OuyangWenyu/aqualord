# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Aqualord is an AOI metadata query project for remote-sensing and water-resources workflows. Its current product boundary is Query GeoJSON input, theoretical Observation Opportunity output, and curated mission metadata for future Asset Query expansion.

Legacy WRM data-source notes are preserved under `reference/` as knowledge and provenance material. They are not runtime product truth. Structured facts used by the query engine live in `aqualord/data/*.json`.

## Environment

```bash
uv sync --dev
uv run pytest
```

Use `uv` for environment management. The legacy environment file has been removed; add runtime and development dependencies through `pyproject.toml`.

The frontend uses npm scripts:

```bash
npm test
npm run lint
npm run build
```

On Windows PowerShell, use `npm.cmd` if script execution policy blocks `npm.ps1`.

## Directory structure

Core directories:

| Directory | Topic |
|-----------|-------|
| `aqualord/` | Python package, CLI, Mission Catalog, Provenance Index, Tracking Index, and opportunity query logic |
| `src/` | Next.js + CesiumJS frontend for interactive coverage exploration |
| `tests/` | Python regression tests |
| `examples/` | sample GeoJSON inputs and output shapes |
| `docs/` | MVP docs, ADRs, agent docs, and legacy-source policy |
| `reference/` | legacy notes retained as source material, not runtime query data |
| `scripts/` | generation and maintenance scripts |
| `skills/` | Codex skill wrappers for Aqualord workflows |

## Data download patterns

Legacy download scripts under `reference/` are historical reference implementations. Do not wire runtime behavior to them without first extracting structured metadata and provenance.

Most legacy download scripts follow one of these approaches:

1. **Python libraries** - HyRiver suite provides high-level access to US water/weather data.
2. **Direct HTTP/wget** - used for MODIS and CMIP6 style provider downloads.
3. **Web service APIs** - `dataretrieval`, `usgs`, and similar provider clients.

## Common tools used across notebooks

- `xarray` for netCDF reading and N-dimensional array manipulation
- `geopandas` for spatial operations
- `matplotlib` / `cartopy` for mapping
- `h5py` for HDF5 files
- `pandas` for tabular data

## Agent skills

### Issue tracker

Issues and PRDs are tracked in GitHub Issues for `OuyangWenyu/aqualord`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the default five-label triage vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, and `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repository with root `CONTEXT.md` and ADRs under `docs/adr/`. See `docs/agents/domain.md`.
