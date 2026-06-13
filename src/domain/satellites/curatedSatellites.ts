import type { SatelliteConfig } from "./types";
import satelliteData from "./curatedSatellites.generated.json";

export const CURATED_SATELLITES: SatelliteConfig[] = satelliteData as SatelliteConfig[];
export const CURATED_NORAD_IDS = CURATED_SATELLITES.map((sat) => sat.noradId);
