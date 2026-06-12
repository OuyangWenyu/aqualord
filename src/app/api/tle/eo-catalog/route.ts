import { NextResponse } from "next/server";

import snapshot from "@/data/eo-catalog-snapshot.json";
import type { TleRecord } from "@/domain/satellites/types";
import { parseTleText } from "@/domain/tle/parseTle";

export const dynamic = "force-dynamic";

type CachePayload = {
  fetchedAt: string;
  records: TleRecord[];
};

const CACHE_TTL_MS = 6 * 60 * 60 * 1000;
const CELESTRAK_RESOURCE_URL = "https://celestrak.org/NORAD/elements/gp.php?GROUP=resource&FORMAT=TLE";
const MAX_VISUAL_RECORDS = 1200;

let cachedPayload: CachePayload | null = null;

export async function GET() {
  if (cachedPayload && Date.now() - new Date(cachedPayload.fetchedAt).getTime() < CACHE_TTL_MS) {
    return NextResponse.json({ ...cachedPayload, cache: "hit" });
  }

  try {
    const response = await fetch(CELESTRAK_RESOURCE_URL, { next: { revalidate: 21600 } });
    if (!response.ok) {
      throw new Error(`CelesTrak returned ${response.status} for EO catalog`);
    }

    const fetchedAt = new Date().toISOString();
    const records = parseTleText(await response.text(), fetchedAt).slice(0, MAX_VISUAL_RECORDS);
    cachedPayload = { fetchedAt, records };

    return NextResponse.json({ ...cachedPayload, cache: "miss" });
  } catch (error) {
    if (cachedPayload) {
      return NextResponse.json({
        ...cachedPayload,
        cache: "stale",
        warning: error instanceof Error ? error.message : "Failed to refresh EO catalog"
      });
    }

    return NextResponse.json({
      fetchedAt: null,
      records: (snapshot as TleRecord[]).slice(0, MAX_VISUAL_RECORDS),
      cache: "snapshot",
      warning: error instanceof Error ? error.message : "Failed to fetch EO catalog"
    });
  }
}
