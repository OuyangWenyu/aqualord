import { satellitePosition } from "../orbits/propagate";
import type { CoverageWindow, CuratedSatellite, GeoPoint } from "../satellites/types";
import { greatCircleDistanceKm } from "./distance";

type PredictOptions = {
  startTime: Date;
  horizonHours: number;
  stepSeconds: number;
};

type OpenWindow = {
  satellite: CuratedSatellite;
  startTime: Date;
  endTime: Date;
  closestTime: Date;
  minDistanceKm: number;
  sampleCount: number;
};

export function nowCoveringCount(satellites: CuratedSatellite[], point: GeoPoint, time: Date): number {
  return satellites.filter((satellite) => isCoveringPoint(satellite, point, time)).length;
}

export function predictCoverageWindows(
  satellites: CuratedSatellite[],
  point: GeoPoint,
  options: PredictOptions
): CoverageWindow[] {
  const stepMs = Math.max(1, options.stepSeconds) * 1000;
  const endTime = new Date(options.startTime.getTime() + Math.max(0, options.horizonHours) * 60 * 60 * 1000);
  const windows: CoverageWindow[] = [];

  for (const satellite of satellites) {
    if (!satellite.tle) {
      continue;
    }

    let openWindow: OpenWindow | null = null;

    for (let sampleMs = options.startTime.getTime(); sampleMs <= endTime.getTime(); sampleMs += stepMs) {
      const sampleTime = new Date(sampleMs);
      const position = satellitePosition(satellite, sampleTime);

      if (!position) {
        openWindow = closeWindow(openWindow, windows);
        continue;
      }

      const distanceKm = greatCircleDistanceKm(point, position);
      const isCovered = distanceKm <= satellite.swathKm / 2;

      if (!isCovered) {
        openWindow = closeWindow(openWindow, windows);
        continue;
      }

      if (!openWindow) {
        openWindow = {
          satellite,
          startTime: sampleTime,
          endTime: sampleTime,
          closestTime: sampleTime,
          minDistanceKm: distanceKm,
          sampleCount: 1
        };
        continue;
      }

      openWindow.endTime = sampleTime;
      openWindow.sampleCount += 1;
      if (distanceKm < openWindow.minDistanceKm) {
        openWindow.minDistanceKm = distanceKm;
        openWindow.closestTime = sampleTime;
      }
    }

    closeWindow(openWindow, windows);
  }

  return windows.sort((left, right) => left.startTime.localeCompare(right.startTime));
}

function isCoveringPoint(satellite: CuratedSatellite, point: GeoPoint, time: Date): boolean {
  const position = satellitePosition(satellite, time);
  return position ? greatCircleDistanceKm(point, position) <= satellite.swathKm / 2 : false;
}

function closeWindow(openWindow: OpenWindow | null, windows: CoverageWindow[]): null {
  if (!openWindow) {
    return null;
  }

  windows.push({
    satellite: openWindow.satellite,
    startTime: openWindow.startTime.toISOString(),
    endTime: openWindow.endTime.toISOString(),
    closestTime: openWindow.closestTime.toISOString(),
    minDistanceKm: Math.round(openWindow.minDistanceKm * 10) / 10,
    sampleCount: openWindow.sampleCount
  });

  return null;
}
