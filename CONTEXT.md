# Aqualord

Aqualord is a water-resources and remote-sensing metadata query context. Its first product boundary is simple spatial metadata lookup for user-provided geometries, not a hydrologic basin registry.

## Language

**Query GeoJSON**:
The canonical spatial input for v0. It may describe a point, polygon, multipolygon, or feature collection supplied by the user.
_Avoid_: Basin AOI, basin registry, hydrologic unit support

**Observation Opportunity**:
A candidate time window in which a platform and sensor may observe the query GeoJSON under the MVP's simplified geometry model.
_Avoid_: Acquisition, tasking, guaranteed image availability

**Opportunity Query**:
A future or near-real-time query that estimates theoretical observation opportunities for the query GeoJSON.
_Avoid_: Historical asset search, STAC item search

**Asset Query**:
A historical or archive query that searches for existing published geospatial data assets.
_Avoid_: Observation opportunity prediction

**STAC Asset**:
An existing or discoverable geospatial data asset represented through STAC Collection, Item, Asset, and Link concepts.
_Avoid_: Observation opportunity

**Mission Catalog**:
The curated metadata graph used to enrich query results. In v0 it is intentionally small and keeps separate fields for provider, program, mission, constellation, platform, sensor, products, and data access.
_Avoid_: Full satellite database, source note ingestion

**Tracking Index**:
A computation-facing mapping from catalog platform identifiers to external orbit-provider lookup identifiers.
_Avoid_: Mission catalog field

**Provenance Index**:
A documentation-facing mapping from catalog fields to sources, retrieval dates, and confidence notes.
_Avoid_: Mission catalog field

**Program**:
A broad Earth-observation initiative or long-running institutional line that may contain multiple missions.
_Avoid_: Mission, platform

**Mission**:
A specific remote-sensing task or mission identity, often containing one or more platforms and sensors.
_Avoid_: Program, dataset

**Constellation**:
A mission-level grouping of multiple platforms that work as a coordinated set or shared observation capability.
_Avoid_: Platform

**Platform**:
A specific satellite or spacecraft carrying one or more sensors.
_Avoid_: Mission, sensor, dataset

**Sensor**:
A payload or observing system on a platform that produces measurements later represented in products.
_Avoid_: Platform

**Products**:
Named processing levels, data products, or representative collections derived from one or more sensors.
_Avoid_: Sensor

**Provider**:
The organization responsible for publishing, operating, or distributing products or data access endpoints.
_Avoid_: Program

**Data Access**:
The URL, API, portal, STAC API, STAC collection reference, or service entry point used to retrieve or discover data.
_Avoid_: Provider
