import { NextResponse } from "next/server";

import snapshot from "@/data/curated-tle-snapshot.json";
import { CURATED_SATELLITES } from "@/domain/satellites/curatedSatellites";
import type { CuratedSatellite, TleRecord } from "@/domain/satellites/types";
import { parseTleText } from "@/domain/tle/parseTle";

export const dynamic = "force-dynamic";

type CachePayload = {
  fetchedAt: string;
  satellites: CuratedSatellite[];
};

const CACHE_TTL_MS = 6 * 60 * 60 * 1000;
const CELESTRAK_CATNR_URL = "https://celestrak.org/NORAD/elements/gp.php";

let cachedPayload: CachePayload | null = null;

export async function GET() {
  if (cachedPayload && Date.now() - new Date(cachedPayload.fetchedAt).getTime() < CACHE_TTL_MS) {
    return NextResponse.json({ ...cachedPayload, cache: "hit" });
  }

  try {
    const fetchedAt = new Date().toISOString();
    const tleRecords = await fetchCuratedTles(fetchedAt);
    const satellites = attachTles(tleRecords);
    cachedPayload = { fetchedAt, satellites };

    return NextResponse.json({ ...cachedPayload, cache: "miss" });
  } catch (error) {
    if (cachedPayload) {
      return NextResponse.json({
        ...cachedPayload,
        cache: "stale",
        warning: error instanceof Error ? error.message : "Failed to refresh curated TLEs"
      });
    }

    const fallback = attachTles(snapshot as TleRecord[]);
    return NextResponse.json({
      fetchedAt: null,
      satellites: fallback,
      cache: "snapshot",
      warning: error instanceof Error ? error.message : "Failed to fetch curated TLEs"
    });
  }
}

async function fetchCuratedTles(fetchedAt: string): Promise<TleRecord[]> {
  const records = await Promise.all(
    CURATED_SATELLITES.map(async (sat) => {
      const url = `${CELESTRAK_CATNR_URL}?CATNR=${sat.noradId}&FORMAT=TLE`;
      const response = await fetch(url, { next: { revalidate: 21600 } });

      if (!response.ok) {
        throw new Error(`CelesTrak returned ${response.status} for ${sat.name}`);
      }

      const text = await response.text();
      const [record] = parseTleText(text, fetchedAt);
      return record;
    })
  );

  return records.filter(Boolean);
}

function attachTles(records: TleRecord[]): CuratedSatellite[] {
  const byNorad = new Map(records.map((record) => [record.noradId, record]));

  return CURATED_SATELLITES.map((sat) => ({
    ...sat,
    tle: byNorad.get(sat.noradId)
  }));
}
