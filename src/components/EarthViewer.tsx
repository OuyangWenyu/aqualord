"use client";

import { useEffect, useMemo, useRef } from "react";
import * as Cesium from "cesium";
import { eciToEcf, gstime, propagate as propagateSatrec, twoline2satrec } from "satellite.js";

import { greatCircleDistanceKm, toDegrees, toRadians } from "@/domain/coverage/distance";
import { propagateTle, satellitePosition } from "@/domain/orbits/propagate";
import type { CoverageWindow, CuratedSatellite, GeoPoint, TleRecord } from "@/domain/satellites/types";

type EarthViewerProps = {
  token: string;
  curated: CuratedSatellite[];
  eoCatalog: TleRecord[];
  selectedPoint: GeoPoint;
  windows: CoverageWindow[];
  activeWindow: CoverageWindow | null;
  showAllFootprints: boolean;
  playbackMultiplier: number;
  onSelectPoint: (point: GeoPoint) => void;
};

const CESIUM_BASE_URL = "https://cesium.com/downloads/cesiumjs/releases/1.132/Build/Cesium/";
const EO_VISUAL_LIMIT = 450;
const DEFAULT_PLAYBACK_MULTIPLIER = 1;
const ORBIT_RING_SAMPLE_COUNT = 240;
const FALLBACK_ORBIT_PERIOD_MINUTES = 100;
const GROUND_TRACK_ORBIT_COUNT = 3;
const GROUND_TRACK_SAMPLE_STEP_SECONDS = 60;

type GroundTrackSample = {
  point: GeoPoint;
  cartesian: Cesium.Cartesian3;
};

export default function EarthViewer({
  token,
  curated,
  eoCatalog,
  selectedPoint,
  windows,
  activeWindow,
  showAllFootprints,
  playbackMultiplier,
  onSelectPoint
}: EarthViewerProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewerRef = useRef<Cesium.Viewer | null>(null);
  const curatedLayerRef = useRef<Cesium.CustomDataSource | null>(null);
  const eoLayerRef = useRef<Cesium.CustomDataSource | null>(null);
  const queryLayerRef = useRef<Cesium.CustomDataSource | null>(null);

  const relatedNoradIds = useMemo(() => {
    if (windows.length === 0) {
      return new Set(curated.map((sat) => sat.noradId));
    }

    return new Set(windows.map((window) => window.satellite.noradId));
  }, [curated, windows]);

  useEffect(() => {
    if (!containerRef.current || viewerRef.current) {
      return;
    }

    window.CESIUM_BASE_URL = CESIUM_BASE_URL;
    Cesium.Ion.defaultAccessToken = token;

    const viewer = new Cesium.Viewer(containerRef.current, {
      animation: false,
      timeline: true,
      geocoder: false,
      homeButton: false,
      sceneModePicker: false,
      baseLayerPicker: true,
      navigationHelpButton: false,
      fullscreenButton: false,
      shouldAnimate: true
    });

    viewer.scene.globe.enableLighting = true;
    viewer.clock.clockRange = Cesium.ClockRange.UNBOUNDED;
    viewer.clock.multiplier = DEFAULT_PLAYBACK_MULTIPLIER;
    viewer.clock.shouldAnimate = true;
    viewer.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(105, 25, 19000000),
      duration: 0
    });

    const curatedLayer = new Cesium.CustomDataSource("curated-satellites");
    const eoLayer = new Cesium.CustomDataSource("eo-catalog");
    const queryLayer = new Cesium.CustomDataSource("query");
    viewer.dataSources.add(eoLayer);
    viewer.dataSources.add(curatedLayer);
    viewer.dataSources.add(queryLayer);

    curatedLayerRef.current = curatedLayer;
    eoLayerRef.current = eoLayer;
    queryLayerRef.current = queryLayer;
    viewerRef.current = viewer;

    const handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
    handler.setInputAction((event: Cesium.ScreenSpaceEventHandler.PositionedEvent) => {
      const point = pickGlobePoint(viewer, event.position);
      if (point) {
        onSelectPoint(point);
      }
    }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

    return () => {
      handler.destroy();
      viewer.destroy();
      viewerRef.current = null;
    };
  }, [onSelectPoint, token]);

  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer) {
      return;
    }

    viewer.clock.multiplier = playbackMultiplier;
    viewer.clock.shouldAnimate = true;

    if (!activeWindow) {
      viewer.clock.currentTime = Cesium.JulianDate.fromDate(new Date());
    }

    viewer.scene.requestRender();
  }, [activeWindow, playbackMultiplier]);

  useEffect(() => {
    const viewer = viewerRef.current;
    const queryLayer = queryLayerRef.current;
    if (!viewer || !queryLayer) {
      return;
    }

    queryLayer.entities.removeAll();
    queryLayer.entities.add({
      id: "selected-point",
      position: Cesium.Cartesian3.fromDegrees(selectedPoint.lon, selectedPoint.lat, 1200),
      point: {
        pixelSize: 13,
        color: Cesium.Color.WHITE,
        outlineColor: Cesium.Color.fromCssColorString("#36d399"),
        outlineWidth: 3,
        heightReference: Cesium.HeightReference.CLAMP_TO_GROUND
      },
      label: {
        text: `${selectedPoint.lat.toFixed(3)}, ${selectedPoint.lon.toFixed(3)}`,
        pixelOffset: new Cesium.Cartesian2(0, -26),
        font: "12px sans-serif",
        fillColor: Cesium.Color.WHITE,
        showBackground: true,
        backgroundColor: Cesium.Color.fromBytes(7, 16, 20, 210)
      }
    });
  }, [selectedPoint]);

  useEffect(() => {
    const viewer = viewerRef.current;
    if (!viewer) {
      return;
    }

    if (!activeWindow) {
      viewer.clock.currentTime = Cesium.JulianDate.fromDate(new Date());
      viewer.clock.shouldAnimate = true;
      return;
    }

    const closest = Cesium.JulianDate.fromDate(new Date(activeWindow.closestTime));
    viewer.clock.currentTime = closest;
    viewer.clock.shouldAnimate = true;
  }, [activeWindow]);

  useEffect(() => {
    const viewer = viewerRef.current;
    const curatedLayer = curatedLayerRef.current;
    const eoLayer = eoLayerRef.current;
    const queryLayer = queryLayerRef.current;
    if (!viewer || !curatedLayer || !eoLayer || !queryLayer) {
      return;
    }

    const time = activeWindow ? new Date(activeWindow.closestTime) : Cesium.JulianDate.toDate(viewer.clock.currentTime);
    curatedLayer.entities.removeAll();
    eoLayer.entities.removeAll();

    drawEoCatalog(eoLayer, eoCatalog);
    drawCuratedSatellites(
      curatedLayer,
      curated,
      selectedPoint,
      relatedNoradIds,
      time,
      showAllFootprints,
      activeWindow
    );
  }, [activeWindow, curated, eoCatalog, playbackMultiplier, relatedNoradIds, selectedPoint, showAllFootprints]);

  return <div ref={containerRef} className="cesium-host" />;
}

declare global {
  interface Window {
    CESIUM_BASE_URL?: string;
  }
}

function drawEoCatalog(layer: Cesium.CustomDataSource, records: TleRecord[]) {
  for (const record of records.slice(0, EO_VISUAL_LIMIT)) {
    layer.entities.add({
      position: dynamicPosition(record),
      point: {
        pixelSize: 3,
        color: Cesium.Color.fromBytes(86, 166, 255, 72),
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      }
    });
  }
}

function drawCuratedSatellites(
  layer: Cesium.CustomDataSource,
  satellites: CuratedSatellite[],
  selectedPoint: GeoPoint,
  relatedNoradIds: Set<number>,
  time: Date,
  showAllFootprints: boolean,
  activeWindow: CoverageWindow | null
) {
  const activeNoradId = activeWindow?.satellite.noradId;

  for (const sat of satellites) {
    const position = satellitePosition(sat, time);
    if (!position) {
      continue;
    }

    const isRelated = relatedNoradIds.has(sat.noradId);
    const isActive = activeNoradId === sat.noradId;
    const distanceKm = greatCircleDistanceKm(selectedPoint, position);
    const isCoveringSelectedPoint = distanceKm <= sat.swathKm / 2;
    const color = isActive
      ? Cesium.Color.fromCssColorString("#36d399")
      : isRelated
        ? Cesium.Color.fromCssColorString("#56a6ff")
        : Cesium.Color.fromBytes(150, 173, 178, 120);

    layer.entities.add({
      id: `sat-${sat.noradId}`,
      name: sat.name,
      position: sat.tle ? dynamicPosition(sat.tle) : undefined,
      point: {
        pixelSize: isActive ? 11 : isRelated ? 8 : 5,
        color,
        outlineColor: Cesium.Color.BLACK,
        outlineWidth: 1,
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      },
      label: {
        text: isActive || isRelated ? sat.name : "",
        pixelOffset: new Cesium.Cartesian2(0, -18),
        font: "12px sans-serif",
        fillColor: Cesium.Color.WHITE,
        showBackground: isActive,
        backgroundColor: Cesium.Color.fromBytes(7, 16, 20, 210),
        disableDepthTestDistance: Number.POSITIVE_INFINITY
      }
    });

    if (isActive || isRelated) {
      const orbitRing = buildOrbitRing(sat, time);
      if (orbitRing.length > 1) {
        layer.entities.add({
          id: `orbit-${sat.noradId}`,
          polyline: {
            positions: orbitRing,
            width: isActive ? 2.5 : 1.25,
            material: color.withAlpha(isActive ? 0.85 : 0.35),
            depthFailMaterial: color.withAlpha(isActive ? 0.28 : 0.12),
            arcType: Cesium.ArcType.NONE
          }
        });
      }
    }

    if (isActive) {
      const groundTrackSegments = buildGroundTrackSegments(sat, time, GROUND_TRACK_ORBIT_COUNT);
      groundTrackSegments.forEach((segment, segmentIndex) => {
        const trackPositions = segment.map((sample) => sample.cartesian);

        if (trackPositions.length > 1) {
          layer.entities.add({
            id: `ground-track-${sat.noradId}-${segmentIndex}`,
            polyline: {
              positions: trackPositions,
              width: 2,
              material: color.withAlpha(0.78),
              clampToGround: true
            }
          });
        }

        const swathHierarchy = buildSwathStrip(segment, sat.swathKm / 2);
        if (swathHierarchy) {
          layer.entities.add({
            id: `swath-strip-${sat.noradId}-${segmentIndex}`,
            polygon: {
              hierarchy: swathHierarchy,
              material: color.withAlpha(0.14),
              outline: true,
              outlineColor: color.withAlpha(0.34),
              classificationType: Cesium.ClassificationType.TERRAIN
            }
          });
        }
      });
    }

    if (showAllFootprints || isActive || isCoveringSelectedPoint) {
      layer.entities.add({
        id: `footprint-${sat.noradId}`,
        polygon: {
          hierarchy: dynamicFootprint(sat, sat.swathKm / 2),
          material: color.withAlpha(isActive ? 0.26 : 0.12),
          outline: true,
          outlineColor: color.withAlpha(0.7),
          classificationType: Cesium.ClassificationType.TERRAIN
        }
      });
    }
  }
}

function buildOrbitRing(sat: CuratedSatellite, centerTime: Date) {
  if (!sat.tle) {
    return [];
  }

  const satrec = twoline2satrec(sat.tle.line1, sat.tle.line2);
  const orbitPeriodMinutes =
    Number.isFinite(satrec.no) && satrec.no > 0 ? (2 * Math.PI) / satrec.no : FALLBACK_ORBIT_PERIOD_MINUTES;
  const positions: Cesium.Cartesian3[] = [];

  for (let index = 0; index <= ORBIT_RING_SAMPLE_COUNT; index += 1) {
    const offsetMinutes = (index / ORBIT_RING_SAMPLE_COUNT) * orbitPeriodMinutes;
    const time = new Date(centerTime.getTime() + offsetMinutes * 60 * 1000);
    const propagated = propagateSatrec(satrec, time);

    if (!propagated || !propagated.position || typeof propagated.position === "boolean") {
      continue;
    }

    const ecf = eciToEcf(propagated.position, gstime(time));
    positions.push(new Cesium.Cartesian3(ecf.x * 1000, ecf.y * 1000, ecf.z * 1000));
  }

  if (positions.length > 1) {
    positions.push(Cesium.Cartesian3.clone(positions[0]));
  }

  return positions;
}

function buildGroundTrackSegments(sat: CuratedSatellite, startTime: Date, orbitCount: number) {
  if (!sat.tle) {
    return [];
  }

  const periodMinutes = orbitPeriodMinutesFromTle(sat.tle);
  const totalSeconds = periodMinutes * orbitCount * 60;
  const sampleCount = Math.floor(totalSeconds / GROUND_TRACK_SAMPLE_STEP_SECONDS);
  const segments: GroundTrackSample[][] = [];
  let currentSegment: GroundTrackSample[] = [];
  let previousPoint: GeoPoint | null = null;

  for (let index = 0; index <= sampleCount; index += 1) {
    const sampleTime = new Date(startTime.getTime() + index * GROUND_TRACK_SAMPLE_STEP_SECONDS * 1000);
    const position = satellitePosition(sat, sampleTime);

    if (!position) {
      pushGroundSegment(segments, currentSegment);
      currentSegment = [];
      previousPoint = null;
      continue;
    }

    const point = { lat: position.lat, lon: position.lon };
    const crossesDateLine = previousPoint ? Math.abs(point.lon - previousPoint.lon) > 180 : false;

    if (crossesDateLine) {
      pushGroundSegment(segments, currentSegment);
      currentSegment = [];
    }

    currentSegment.push({
      point,
      cartesian: Cesium.Cartesian3.fromDegrees(point.lon, point.lat, 0)
    });
    previousPoint = point;
  }

  pushGroundSegment(segments, currentSegment);
  return segments;
}

function buildSwathStrip(samples: GroundTrackSample[], halfSwathKm: number) {
  if (samples.length < 2) {
    return null;
  }

  const left: Cesium.Cartesian3[] = [];
  const right: Cesium.Cartesian3[] = [];

  for (let index = 0; index < samples.length; index += 1) {
    const previous = samples[Math.max(0, index - 1)].point;
    const current = samples[index].point;
    const next = samples[Math.min(samples.length - 1, index + 1)].point;
    const bearing = bearingRadians(previous, next);

    const leftPoint = destinationPoint(current, halfSwathKm, bearing - Math.PI / 2);
    const rightPoint = destinationPoint(current, halfSwathKm, bearing + Math.PI / 2);

    left.push(Cesium.Cartesian3.fromDegrees(leftPoint.lon, leftPoint.lat, 0));
    right.push(Cesium.Cartesian3.fromDegrees(rightPoint.lon, rightPoint.lat, 0));
  }

  return new Cesium.PolygonHierarchy([...left, ...right.reverse()]);
}

function pushGroundSegment(segments: GroundTrackSample[][], segment: GroundTrackSample[]) {
  if (segment.length > 1) {
    segments.push(segment);
  }
}

function orbitPeriodMinutesFromTle(tle: TleRecord) {
  const satrec = twoline2satrec(tle.line1, tle.line2);
  return Number.isFinite(satrec.no) && satrec.no > 0
    ? (2 * Math.PI) / satrec.no
    : FALLBACK_ORBIT_PERIOD_MINUTES;
}

function dynamicPosition(tle: TleRecord) {
  return new Cesium.CallbackPositionProperty((time) => {
    const currentTime = time ?? Cesium.JulianDate.now();
    const position = propagateTle(tle, Cesium.JulianDate.toDate(currentTime));
    if (!position) {
      return undefined;
    }

    return Cesium.Cartesian3.fromDegrees(position.lon, position.lat, position.altitudeKm * 1000);
  }, false);
}

function dynamicFootprint(sat: CuratedSatellite, radiusKm: number) {
  return new Cesium.CallbackProperty((time) => {
    const currentTime = time ?? Cesium.JulianDate.now();
    const position = satellitePosition(sat, Cesium.JulianDate.toDate(currentTime));
    if (!position) {
      return undefined;
    }

    return new Cesium.PolygonHierarchy(buildFootprint(position, radiusKm, 96));
  }, false);
}

function buildFootprint(center: GeoPoint, radiusKm: number, segments: number) {
  const points: Cesium.Cartesian3[] = [];

  for (let i = 0; i < segments; i += 1) {
    const bearing = (2 * Math.PI * i) / segments;
    const point = destinationPoint(center, radiusKm, bearing);
    points.push(Cesium.Cartesian3.fromDegrees(point.lon, point.lat, 0));
  }

  return points;
}

function destinationPoint(point: GeoPoint, distanceKm: number, bearingRad: number): GeoPoint {
  const angularDistance = distanceKm / 6371.0088;
  const lat1 = toRadians(point.lat);
  const lon1 = toRadians(point.lon);

  const lat2 = Math.asin(
    Math.sin(lat1) * Math.cos(angularDistance) +
      Math.cos(lat1) * Math.sin(angularDistance) * Math.cos(bearingRad)
  );
  const lon2 =
    lon1 +
    Math.atan2(
      Math.sin(bearingRad) * Math.sin(angularDistance) * Math.cos(lat1),
      Math.cos(angularDistance) - Math.sin(lat1) * Math.sin(lat2)
    );

  return {
    lat: toDegrees(lat2),
    lon: ((((toDegrees(lon2) + 180) % 360) + 360) % 360) - 180
  };
}

function bearingRadians(from: GeoPoint, to: GeoPoint) {
  const lat1 = toRadians(from.lat);
  const lat2 = toRadians(to.lat);
  const dLon = toRadians(to.lon - from.lon);
  const y = Math.sin(dLon) * Math.cos(lat2);
  const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
  return Math.atan2(y, x);
}

function pickGlobePoint(viewer: Cesium.Viewer, position: Cesium.Cartesian2): GeoPoint | null {
  const scene = viewer.scene;
  const ray = viewer.camera.getPickRay(position);
  const cartesian = ray ? scene.globe.pick(ray, scene) : viewer.camera.pickEllipsoid(position, scene.globe.ellipsoid);

  if (!cartesian) {
    return null;
  }

  const cartographic = Cesium.Cartographic.fromCartesian(cartesian);
  return {
    lat: Cesium.Math.toDegrees(cartographic.latitude),
    lon: Cesium.Math.toDegrees(cartographic.longitude)
  };
}
