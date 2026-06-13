# Aqualord

English | [简体中文](README.zh-CN.md)

Aqualord is an AOI metadata query project for remote-sensing and water-resources workflows. The current product boundary is Query GeoJSON input, theoretical Observation Opportunity output, and curated mission metadata that can later connect to historical Asset Query paths.

It is not a general hydrologic basin registry and it is not yet a historical archive or STAC Item search engine.

References:

- [Satellite Remote Sensing for Water Resources Management: Potential for Supporting Sustainable Development in Data-Poor Regions](https://doi.org/10.1029/2017WR022437)
- [Applied Remote Sensing Training](https://arset.gsfc.nasa.gov/)
- [FrontierDevelopmentLab/sat-extractor](https://github.com/FrontierDevelopmentLab/sat-extractor)

## Contents

- `aqualord/`: Python package and CLI for opportunity queries, catalog loading, orbit providers, tracking indexes, and provenance.
- `src/`: Next.js + CesiumJS frontend for interactive satellite coverage exploration.
- `tests/`: Python regression tests for the CLI, catalog generation, provenance, and orbit providers.
- `examples/`: sample GeoJSON input and opportunity result shapes.
- `docs/`: MVP boundaries, ADRs, agent docs, and legacy-source policy.
- `reference/`: legacy data-source notes preserved as knowledge and provenance material.
- `scripts/`: supporting generation and maintenance scripts.
- `skills/`: Codex skill routing natural-language opportunity questions to the CLI.

Legacy notes previously stored as root-level data-source directories now live under `reference/`. They are not runtime product truth; structured facts used by queries live in `aqualord/data/*.json`.

## Python Environment

The Python project uses `uv`:

```shell
uv sync --dev
uv run pytest
```

Install the CLI as a global uv tool:

```shell
uv tool install --editable D:\Code\aqualord --force
aqualord opportunities --geo examples\query-dalian.geojson --hours 48 --format json
```

## JavaScript Environment

The frontend uses npm scripts:

```shell
npm install
npm run dev
npm test
npm run lint
npm run build
```

On Windows PowerShell, use `npm.cmd` if the script execution policy blocks `npm.ps1`.

## Observation Opportunity MVP

Aqualord includes a Python CLI and a Next.js + CesiumJS MVP for potential remote-sensing satellite coverage queries. It uses curated mission metadata, CelesTrak TLE data, and `satellite.js` to estimate geometric coverage for a selected ground point or query geometry.

Core workflow:

- Select a point on the 3D globe or enter latitude/longitude.
- Query current potential coverage from curated earth-observation satellites.
- Predict potential coverage windows for the next 72 hours.
- Visualize satellites, orbit rings, ground tracks, swath strips, and footprints in Cesium.

Configure a Cesium Ion token:

```shell
cp .env.example .env.local
```

Then set:

```shell
CESIUM_TOKEN=your_cesium_ion_token_here
```

Run the web app:

```shell
npm install
npm run dev
```

Open `http://localhost:3000`.

The MVP reports only geometric potential coverage. It does not evaluate cloud cover, day/night conditions, off-nadir tasking, SAR imaging modes, scheduling constraints, or actual data availability.

## Legacy Knowledge Sources

The historical WRM notes are preserved under `reference/` as source material. See `reference/README.md` for the source index and `docs/legacy-knowledge-sources.md` for the migration policy.

## Contribution

1. Fork this repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.
