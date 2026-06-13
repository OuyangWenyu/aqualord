# Legacy Knowledge Sources

Aqualord is now an AOI metadata query tool for user-provided Query GeoJSON. The legacy data-source notes are retained as knowledge and provenance sources, not as the runtime data model.

Structured facts that affect query behavior live in `aqualord/data/*.json`. Legacy Markdown, notebooks, scripts, images, and PDFs under `reference/` are source material for future catalog curation, provenance review, Asset Query work, and tutorials.

## Policy

- Keep legacy notes out of the repository root so the root reflects the active product.
- Preserve each moved directory's internal layout to avoid breaking relative Markdown and notebook links.
- Do not delete screenshots, PDFs, notebooks, or scripts during the first reorganization pass.
- Do not treat a legacy note as product truth until the relevant fields have been extracted into the Mission Catalog and Provenance Index.
- Record extracted facts with source names, source URLs, retrieval dates, and confidence notes.

## Status Labels

| Status | Meaning |
| --- | --- |
| `catalog-partial` | Some facts are already represented in the Mission Catalog or Provenance Index, but the source still needs review before it can be considered exhausted. |
| `catalog-candidate` | The source is relevant to future Mission Catalog enrichment but is not yet represented as structured product data. |
| `asset-query-candidate` | The source may support a future STAC-backed or provider-backed historical Asset Query path. |
| `reference-only` | The source is background, tutorial, market, or workflow material and should not drive runtime query behavior directly. |
| `archive-candidate` | The source appears to be local residue or obsolete material and should be reviewed separately before deletion. |

## First-Pass Classification

| Source | New location | Status | Notes |
| --- | --- | --- | --- |
| `Landsat/` | `reference/opportunity-sources/landsat/` | `catalog-partial` | Landsat 8 and Landsat 9 are represented in the current Mission Catalog. |
| `MODIS/` | `reference/opportunity-sources/modis/` | `catalog-partial` | Terra/Aqua MODIS entries exist; download notes and scripts remain useful for future Asset Query work. |
| `SMAP/` | `reference/opportunity-sources/smap/` | `catalog-partial` | SMAP metadata exists; notebooks and screenshots remain provenance material. |
| `ICESat/` | `reference/opportunity-sources/icesat/` | `catalog-candidate` | Altimetry source material, not yet a completed catalog extraction. |
| `GRACE/` | `reference/asset-query-sources/grace/` | `catalog-candidate` | Gravity mission notes may inform future catalog or asset work. |
| `CAMELS/` | `reference/asset-query-sources/camels/` | `asset-query-candidate` | Hydrologic sample dataset material for future asset-oriented flows. |
| `GAGES/` | `reference/asset-query-sources/gages/` | `asset-query-candidate` | USGS streamflow and reference basin notes. |
| `Daymet/` | `reference/asset-query-sources/daymet/` | `asset-query-candidate` | Meteorological forcing source material. |
| `NH/` | `reference/asset-query-sources/nh/` | `asset-query-candidate` | NHDPlus, 3DEP, WBD, and related hydrologic reference material. |
| `NLCD/` | `reference/asset-query-sources/nlcd/` | `asset-query-candidate` | Land-cover asset source material. |
| `HydroSHEDS/` | `reference/asset-query-sources/hydrosheds/` | `asset-query-candidate` | Global hydrography source material. |
| `LDAS/` | `reference/asset-query-sources/ldas/` | `asset-query-candidate` | Land data assimilation notes. |
| `CMIP6/` | `reference/asset-query-sources/cmip6/` | `asset-query-candidate` | Climate model data access notes and script. |
| `DAM/` | `reference/asset-query-sources/dam/` | `asset-query-candidate` | Dam and reservoir dataset notes. |
| `DEM/` | `reference/asset-query-sources/dem/` | `asset-query-candidate` | Digital elevation source notes. |
| `Electric/` | `reference/domain-notes/electric/` | `reference-only` | Water-adjacent domain background, not an AOI metadata source. |
| `ARSET/` | `reference/tutorials/arset/` | `reference-only` | NASA training notes and screenshots. |
| `DataFormat/` | `reference/tutorials/data-format/` | `reference-only` | netCDF/HDF5 tutorial material. |
| `Tools/` | `reference/tutorials/tools/` | `reference-only` | Tooling and market reference notes. |
| `WebService/` | `reference/tutorials/web-service/` | `reference-only` | Cloud and service access examples. |
| `EOMarket/` | not migrated | `archive-candidate` | Current tree only contains ignored `.ipynb_checkpoints/` residue, with no tracked source files. |

## Follow-Up Cleanup

Image, PDF, and notebook-output cleanup should be a separate pass. That pass should first generate an asset inventory, identify which files are referenced by Markdown or notebooks, and only then delete or compress low-value assets.
