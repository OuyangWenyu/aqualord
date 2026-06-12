# Data for WRM

Aqualord is a reference repository for Water Resources Management (WRM) data sources. It records remote sensing, hydrology, and climate datasets, including basic descriptions, access methods, and processing notes where examples exist.

References:

- [Satellite Remote Sensing for Water Resources Management: Potential for Supporting Sustainable Development in Data-Poor Regions](https://doi.org/10.1029/2017WR022437)
- [Applied Remote Sensing Training](https://arset.gsfc.nasa.gov/)
- [FrontierDevelopmentLab/sat-extractor](https://github.com/FrontierDevelopmentLab/sat-extractor)

## Contents

- `ARSET/`: NASA Applied Remote Sensing training materials
- `CAMELS/`: large-sample catchment hydrology datasets
- `CMIP6/`: NEX-GDDP-CMIP6 downscaled climate data
- `DAM/`: dam and reservoir datasets
- `DataFormat/`: netCDF and HDF5 notes
- `Daymet/`: daily meteorological forcing data
- `DEM/`: digital elevation data
- `Electric/`: US electric grid data relevant to water
- `EOMarket/`: earth observation market platform notes
- `GAGES/`: USGS streamflow reference datasets
- `GRACE/`: Gravity Recovery and Climate Experiment data
- `HydroSHEDS/`: hydrological SRTM-derived datasets
- `ICESat/`: laser altimetry for inland water bodies
- `Landsat/`: Landsat mission overview
- `LDAS/`: NASA Land Data Assimilation System
- `MODIS/`: MODIS product notes and download scripts
- `NH/`: US National Hydrography datasets
- `NLCD/`: US National Land Cover Database
- `SMAP/`: NASA soil moisture satellite data
- `WebService/`: cloud data access notes

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

## Satellite Coverage MVP

This branch also includes a Next.js + CesiumJS MVP for potential remote-sensing satellite coverage queries. It uses CelesTrak TLE data and `satellite.js` to estimate geometric coverage for a selected ground point.

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

## Contribution

1. Fork this repository.
2. Create a feature branch.
3. Commit changes.
4. Open a pull request.
