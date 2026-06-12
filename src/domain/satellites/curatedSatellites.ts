import type { SatelliteConfig } from "./types";

export const CURATED_SATELLITES: SatelliteConfig[] = [
  {
    noradId: 40697,
    name: "Sentinel-2A",
    operator: "ESA",
    sensorType: "multispectral",
    swathKm: 290,
    resolutionM: 10,
    revisitDays: 5,
    source: "ESA Sentinel-2 MSI public mission specifications"
  },
  {
    noradId: 42063,
    name: "Sentinel-2B",
    operator: "ESA",
    sensorType: "multispectral",
    swathKm: 290,
    resolutionM: 10,
    revisitDays: 5,
    source: "ESA Sentinel-2 MSI public mission specifications"
  },
  {
    noradId: 39084,
    name: "Landsat 8",
    operator: "NASA/USGS",
    sensorType: "multispectral",
    swathKm: 185,
    resolutionM: 30,
    revisitDays: 16,
    source: "USGS Landsat 8 public mission specifications"
  },
  {
    noradId: 49260,
    name: "Landsat 9",
    operator: "NASA/USGS",
    sensorType: "multispectral",
    swathKm: 185,
    resolutionM: 30,
    revisitDays: 16,
    source: "USGS Landsat 9 public mission specifications"
  },
  {
    noradId: 39634,
    name: "Sentinel-1A",
    operator: "ESA",
    sensorType: "sar",
    swathKm: 250,
    resolutionM: 5,
    revisitDays: 12,
    source: "ESA Sentinel-1 IW mode public mission specifications",
    notes: "MVP uses a representative IW mode swath."
  },
  {
    noradId: 41335,
    name: "Sentinel-3A",
    operator: "ESA/EUMETSAT",
    sensorType: "multispectral",
    swathKm: 1270,
    resolutionM: 300,
    revisitDays: 2,
    source: "ESA Sentinel-3 OLCI public mission specifications"
  },
  {
    noradId: 43437,
    name: "Sentinel-3B",
    operator: "ESA/EUMETSAT",
    sensorType: "multispectral",
    swathKm: 1270,
    resolutionM: 300,
    revisitDays: 2,
    source: "ESA Sentinel-3 OLCI public mission specifications"
  },
  {
    noradId: 25994,
    name: "Terra",
    operator: "NASA",
    sensorType: "multispectral",
    swathKm: 2330,
    resolutionM: 250,
    revisitDays: 1,
    source: "NASA MODIS public mission specifications"
  },
  {
    noradId: 27424,
    name: "Aqua",
    operator: "NASA",
    sensorType: "multispectral",
    swathKm: 2330,
    resolutionM: 250,
    revisitDays: 1,
    source: "NASA MODIS public mission specifications"
  },
  {
    noradId: 37849,
    name: "Suomi NPP",
    operator: "NOAA/NASA",
    sensorType: "weather",
    swathKm: 3060,
    resolutionM: 375,
    revisitDays: 1,
    source: "NOAA/NASA VIIRS public mission specifications"
  },
  {
    noradId: 43013,
    name: "NOAA-20",
    operator: "NOAA",
    sensorType: "weather",
    swathKm: 3060,
    resolutionM: 375,
    revisitDays: 1,
    source: "NOAA VIIRS public mission specifications"
  },
  {
    noradId: 54234,
    name: "NOAA-21",
    operator: "NOAA",
    sensorType: "weather",
    swathKm: 3060,
    resolutionM: 375,
    revisitDays: 1,
    source: "NOAA VIIRS public mission specifications"
  },
  {
    noradId: 43641,
    name: "SAOCOM 1A",
    operator: "CONAE",
    sensorType: "sar",
    swathKm: 350,
    resolutionM: 10,
    revisitDays: 8,
    source: "CONAE SAOCOM public mission specifications",
    notes: "MVP uses a representative wide mode swath."
  },
  {
    noradId: 46984,
    name: "SAOCOM 1B",
    operator: "CONAE",
    sensorType: "sar",
    swathKm: 350,
    resolutionM: 10,
    revisitDays: 8,
    source: "CONAE SAOCOM public mission specifications",
    notes: "MVP uses a representative wide mode swath."
  }
];

export const CURATED_NORAD_IDS = CURATED_SATELLITES.map((sat) => sat.noradId);
