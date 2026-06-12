import { describe, expect, it } from "vitest";

import { noradIdFromLine1, parseTleText } from "./parseTle";

describe("parseTleText", () => {
  it("parses records and extracts NORAD IDs", () => {
    const records = parseTleText(`ISS (ZARYA)
1 25544U 98067A   26162.50000000  .00016717  00000+0  10270-3 0  9000
2 25544  51.6400 120.0000 0005000  90.0000 270.0000 15.50000000  0000`);

    expect(records).toHaveLength(1);
    expect(records[0].noradId).toBe(25544);
  });
});

describe("noradIdFromLine1", () => {
  it("returns null for invalid line one values", () => {
    expect(noradIdFromLine1("bad")).toBeNull();
  });
});
