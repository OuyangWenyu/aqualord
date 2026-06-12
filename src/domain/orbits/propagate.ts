import {
  degreesLat,
  degreesLong,
  eciToGeodetic,
  gstime,
  propagate,
  twoline2satrec
} from "satellite.js";

import type { CuratedSatellite, SatellitePosition, TleRecord } from "../satellites/types";

export function propagateTle(tle: TleRecord, time: Date) {
  const satrec = twoline2satrec(tle.line1, tle.line2);
  const result = propagate(satrec, time);

  if (!result || !result.position || typeof result.position === "boolean") {
    return null;
  }

  const gmst = gstime(time);
  const geo = eciToGeodetic(result.position, gmst);

  return {
    lat: degreesLat(geo.latitude),
    lon: normalizeLongitude(degreesLong(geo.longitude)),
    altitudeKm: geo.height
  };
}

export function satellitePosition(sat: CuratedSatellite, time: Date): SatellitePosition | null {
  if (!sat.tle) {
    return null;
  }

  const propagated = propagateTle(sat.tle, time);
  if (!propagated) {
    return null;
  }

  return {
    sat,
    time,
    ...propagated
  };
}

export function normalizeLongitude(lon: number): number {
  const normalized = ((((lon + 180) % 360) + 360) % 360) - 180;
  return Object.is(normalized, -0) ? 0 : normalized;
}
