# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project overview

Aqualord is a Chinese-language reference repository cataloging data sources for Water Resources Management (WRM). It documents remote sensing, hydrology, and climate datasets — their characteristics, download methods, and (where used) processing workflows. Content is organized as Markdown notes paired with executable Jupyter notebooks or standalone Python scripts.

## Environment

```bash
uv sync --dev
uv run pytest
```

Use `uv` for environment management. The legacy environment file has been removed; add runtime and development dependencies through `pyproject.toml`.

## Directory structure

Each top-level directory covers one data source or topic:

| Directory | Topic |
|-----------|-------|
| `ARSET/` | NASA Applied Remote Sensing training materials |
| `CAMELS/` | Catchment Attributes and MEteorology for Large-sample Studies |
| `CMIP6/` | Climate Model Intercomparison Project (NEX-GDDP-CMIP6 downscaled) |
| `DAM/` | Dam/reservoir datasets (NID) |
| `DataFormat/` | Working with netCDF and HDF5 in Python |
| `Daymet/` | Daily meteorological forcing data (source for CAMELS) |
| `DEM/` | Digital Elevation Model sources |
| `EOMarket/` | Earth Observation market platform summaries |
| `Electric/` | US electric grid data relevant to water |
| `GAGES/` | USGS streamflow reference datasets |
| `GRACE/` | Gravity Recovery and Climate Experiment |
| `HydroSHEDS/` | Hydrological SRTM-derived data |
| `ICESat/` | Ice/laser altimetry for inland water bodies |
| `Landsat/` | Landsat mission overview |
| `LDAS/` | NASA Land Data Assimilation System (NLDAS) |
| `MODIS/` | MODIS product download with `get_modis.py` |
| `NH/` | US National Hydrography (NHDPlus, 3DEP) |
| `NLCD/` | US National Land Cover Database |
| `SMAP/` | NASA Soil Moisture Active Passive |
| `WebService/` | Cloud data access (Google Drive, Kaggle, async retriever) |
| `Tools/` | Reference materials and screenshots |

## Data download patterns

Most download scripts follow one of these approaches:

1. **Python libraries** — HyRiver suite provides high-level access to US water/weather data (Daymet, NWIS, NHD, 3DEP, NLCD). Preferred when available.
2. **Direct HTTP/wget** — Used for MODIS (USGS EarthData), CMIP6 (NASA THREDDS NCSS). EarthData sources require authentication.
3. **Web service APIs** — `dataretrieval` for USGS water data, `usgs` package for EarthExplorer, `smap_io` for SMAP.

## Common tools used across notebooks

- `xarray` for netCDF reading and N-dimensional array manipulation
- `geopandas` for spatial operations
- `matplotlib` / `cartopy` for mapping
- `h5py` for HDF5 files
- `pandas` for tabular data
