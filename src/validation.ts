import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_PATH = join(__dirname, "..", "data", "dataset.json");

export const TaxiTripSchema = z.object({
  id: z.string(),
  pickup_zone: z.string(),
  pickup_lat: z.number(),
  pickup_lon: z.number(),
  dropoff_zone: z.string(),
  dropoff_lat: z.number(),
  dropoff_lon: z.number(),
  pickup_time: z.string(),
  dropoff_time: z.string(),
  distance_miles: z.number().min(0),
  duration_seconds: z.number().int().min(0),
  fare_amount: z.number().min(0),
  tolls_amount: z.number().min(0),
  tip_amount: z.number().min(0),
  total_amount: z.number().min(0),
  payment_type: z.string(),
  rate_code: z.number().int(),
  passenger_count: z.number().int().min(1).max(6),
  vendor_id: z.string(),
});

export const DatasetSchema = z.array(TaxiTripSchema);
export type TaxiTrip = z.infer<typeof TaxiTripSchema>;

export function loadAndValidate(): { valid: TaxiTrip[]; errors: z.ZodError[] } {
  const raw = JSON.parse(readFileSync(DATA_PATH, "utf-8"));
  const valid: TaxiTrip[] = [];
  const errors: z.ZodError[] = [];
  for (const item of raw) {
    const result = TaxiTripSchema.safeParse(item);
    if (result.success) {
      valid.push(result.data);
    } else {
      errors.push(result.error);
    }
  }
  return { valid, errors };
}

export function validateRecord(record: unknown): record is TaxiTrip {
  return TaxiTripSchema.safeParse(record).success;
}
