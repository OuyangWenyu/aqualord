export type SensorType = "optical" | "sar" | "multispectral" | "thermal" | "weather";

export type SatelliteConfig = {
  noradId: number;
  name: string;
  operator: string;
  sensorType: SensorType;
  swathKm: number;
  resolutionM: number;
  revisitDays?: number;
  source: string;
  notes?: string;
};

export type TleRecord = {
  name: string;
  noradId: number;
  line1: string;
  line2: string;
  fetchedAt?: string;
};

export type CuratedSatellite = SatelliteConfig & {
  tle?: TleRecord;
};

export type GeoPoint = {
  lat: number;
  lon: number;
};

export type SatellitePosition = {
  sat: CuratedSatellite;
  time: Date;
  lat: number;
  lon: number;
  altitudeKm: number;
};

export type CoverageWindow = {
  satellite: CuratedSatellite;
  startTime: string;
  endTime: string;
  closestTime: string;
  minDistanceKm: number;
  sampleCount: number;
};
