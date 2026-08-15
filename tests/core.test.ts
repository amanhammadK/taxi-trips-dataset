import { describe, it, expect } from "vitest";
import { query, getRecord, stats } from "../src/core.js";

describe("dataset core", () => {
  it("query returns results", async () => {
    const results = await query({});
    expect(Array.isArray(results.records)).toBe(true);
  });

  it("getRecord returns single record", async () => {
    const all = await query({});
    if (all.records.length > 0) {
      const record = await getRecord(all.records[0].id);
      expect(record).toBeTruthy();
    }
  });

  it("stats returns summary", async () => {
    const s = await stats();
    expect(s).toBeDefined();
    expect(s).toHaveProperty("count");
  });
});
