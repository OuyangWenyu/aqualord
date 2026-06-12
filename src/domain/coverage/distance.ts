import type { GeoPoint } from "../satellites/types";

const EARTH_RADIUS_KM = 6371.0088;

export function toRadians(degrees: number): number {
  return (degrees * Math.PI) / 180;
}

export function toDegrees(radians: number): number {
  return (radians * 180) / Math.PI;
}

export function isValidGeoPoint(point: GeoPoint): boolean {
  return (
    Number.isFinite(point.lat) &&
    Number.isFinite(point.lon) &&
    point.lat >= -90 &&
    point.lat <= 90 &&
    point.lon >= -180 &&
    point.lon <= 180
  );
}

export function greatCircleDistanceKm(from: GeoPoint, to: GeoPoint): number {
  const fromLat = toRadians(from.lat);
  const toLat = toRadians(to.lat);
  const deltaLat = toRadians(to.lat - from.lat);
  const deltaLon = toRadians(to.lon - from.lon);

  const halfChord =
    Math.sin(deltaLat / 2) ** 2 +
    Math.cos(fromLat) * Math.cos(toLat) * Math.sin(deltaLon / 2) ** 2;
  const centralAngle = 2 * Math.atan2(Math.sqrt(halfChord), Math.sqrt(1 - halfChord));

  return EARTH_RADIUS_KM * centralAngle;
}
