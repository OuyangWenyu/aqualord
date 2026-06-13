import json
from pathlib import Path
from typing import Any


SUPPORTED_TYPES = {"Point", "Polygon", "MultiPolygon", "Feature", "FeatureCollection"}


def load_query_geojson(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("Query GeoJSON must be a JSON object.")

    geo_type = data.get("type")
    if geo_type not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported Query GeoJSON type: {geo_type!r}")

    geometry = _primary_geometry(data)
    coordinates = geometry.get("coordinates")
    if coordinates is None:
        raise ValueError("Query GeoJSON geometry must include coordinates.")

    points = _flatten_points(coordinates)
    if not points:
        raise ValueError("Query GeoJSON geometry does not contain coordinates.")

    bbox = _bbox(points)
    return {
        "type": geometry["type"],
        "bbox": bbox,
        "centroid": _centroid_for_geometry(geometry["type"], coordinates, bbox),
    }


def _primary_geometry(data: dict[str, Any]) -> dict[str, Any]:
    geo_type = data["type"]
    if geo_type == "Feature":
        geometry = data.get("geometry")
        if not isinstance(geometry, dict):
            raise ValueError("GeoJSON Feature must include a geometry object.")
        if geometry.get("type") not in {"Point", "Polygon", "MultiPolygon"}:
            raise ValueError(f"Unsupported Feature geometry type: {geometry.get('type')!r}")
        return geometry

    if geo_type == "FeatureCollection":
        features = data.get("features")
        if not isinstance(features, list) or not features:
            raise ValueError("GeoJSON FeatureCollection must include at least one feature.")
        geometries = [_primary_geometry(feature) for feature in features]
        points = []
        for geometry in geometries:
            points.extend(_flatten_points(geometry["coordinates"]))
        bbox = _bbox(points)
        return {
            "type": "FeatureCollection",
            "coordinates": [[bbox[0], bbox[1]], [bbox[2], bbox[3]]],
        }

    return data


def _flatten_points(coordinates: Any) -> list[list[float]]:
    if (
        isinstance(coordinates, list)
        and len(coordinates) >= 2
        and isinstance(coordinates[0], (int, float))
        and isinstance(coordinates[1], (int, float))
    ):
        return [[float(coordinates[0]), float(coordinates[1])]]

    points: list[list[float]] = []
    if isinstance(coordinates, list):
        for item in coordinates:
            points.extend(_flatten_points(item))
    return points


def _bbox(points: list[list[float]]) -> list[float]:
    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    return [min(xs), min(ys), max(xs), max(ys)]


def _centroid_for_geometry(geo_type: str, coordinates: Any, bbox: list[float]) -> list[float]:
    if geo_type == "Point":
        point = _flatten_points(coordinates)[0]
        return [point[0], point[1]]

    return [
        (bbox[0] + bbox[2]) / 2,
        (bbox[1] + bbox[3]) / 2,
    ]
