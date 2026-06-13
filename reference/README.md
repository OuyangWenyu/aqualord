# Reference Sources

This directory contains legacy Aqualord notes. They are preserved as knowledge sources for catalog curation, provenance checks, future Asset Query work, and tutorials.

The active product is the AOI metadata query engine in `aqualord/` and `src/`. Runtime query behavior should use structured data from `aqualord/data/*.json`, not unstructured notes in this directory.

## Layout

| Directory | Role |
| --- | --- |
| `opportunity-sources/` | Satellite and sensor source notes that may support Observation Opportunity metadata. |
| `asset-query-sources/` | Hydrology, climate, terrain, and data-asset notes for a future historical Asset Query path. |
| `domain-notes/` | Water-adjacent background material that does not directly define query behavior. |
| `tutorials/` | Training, file-format, and service-access notes. |

## Source Index

A complete per-source index with status labels, original locations, and notes is in `docs/legacy-knowledge-sources.md`. See that file for the migration policy and status definitions.
