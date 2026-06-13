# Separate Observation Opportunities from STAC Assets

Status: accepted

Aqualord v0 treats future and near-real-time overpass analysis as observation opportunity detection, not as STAC asset search. STAC is the preferred direction for historical or published geospatial assets, but predicted opportunities are not STAC Items because they do not confirm acquisition, processing, publication, or downloadable assets.

## Considered Options

- Model predicted opportunities as STAC Items. Rejected because STAC Items describe discoverable data assets, while v0 opportunities are theoretical candidates.
- Build a custom historical asset schema. Rejected because STAC already standardizes Collections, Items, Assets, and Links for this role.
- Split the system into an opportunity path and a later STAC-backed asset path. Chosen because it keeps the MVP focused while preserving compatibility with existing geospatial asset standards.

## Consequences

MVP v0 query results may point to possible products and STAC collection entry points, but they must not claim that an image exists. Historical archive search should be implemented as a separate STAC-backed asset query path in a later version.

