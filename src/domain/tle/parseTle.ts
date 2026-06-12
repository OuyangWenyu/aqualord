import type { TleRecord } from "../satellites/types";

export function noradIdFromLine1(line1: string): number | null {
  const match = /^1\s+(\d{5})/.exec(line1.trim());
  return match ? Number(match[1]) : null;
}

export function parseTleText(text: string, fetchedAt?: string): TleRecord[] {
  const lines = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  const records: TleRecord[] = [];

  for (let i = 0; i < lines.length - 2; i += 1) {
    const name = lines[i];
    const line1 = lines[i + 1];
    const line2 = lines[i + 2];

    if (!line1.startsWith("1 ") || !line2.startsWith("2 ")) {
      continue;
    }

    const noradId = noradIdFromLine1(line1);
    if (!noradId) {
      continue;
    }

    records.push({ name, noradId, line1, line2, fetchedAt });
    i += 2;
  }

  return records;
}

export function indexTlesByNorad(records: TleRecord[]): Map<number, TleRecord> {
  return new Map(records.map((record) => [record.noradId, record]));
}
