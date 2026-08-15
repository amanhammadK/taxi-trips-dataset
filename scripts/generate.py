import json, random, os, math
from pathlib import Path
from datetime import datetime, timedelta

HERE = Path(__file__).parent
DATA_DIR = HERE.parent / "data"

def gen_taxi(n=2000):
    random.seed(42)
    pickup_locations = [
        {"zone": "Midtown Manhattan", "lat": 40.7549, "lon": -73.9840, "weight": 0.15},
        {"zone": "Times Square", "lat": 40.7580, "lon": -73.9855, "weight": 0.12},
        {"zone": "JFK Airport", "lat": 40.6413, "lon": -73.7781, "weight": 0.08},
        {"zone": "LaGuardia Airport", "lat": 40.7769, "lon": -73.8740, "weight": 0.06},
        {"zone": "Penn Station", "lat": 40.7506, "lon": -73.9935, "weight": 0.10},
        {"zone": "Wall Street", "lat": 40.7074, "lon": -74.0113, "weight": 0.09},
        {"zone": "Brooklyn Heights", "lat": 40.6960, "lon": -73.9936, "weight": 0.05},
        {"zone": "Harlem", "lat": 40.8116, "lon": -73.9465, "weight": 0.04},
        {"zone": "Greenwich Village", "lat": 40.7336, "lon": -74.0027, "weight": 0.06},
        {"zone": "Upper East Side", "lat": 40.7736, "lon": -73.9566, "weight": 0.05},
        {"zone": "Chelsea", "lat": 40.7465, "lon": -74.0014, "weight": 0.05},
        {"zone": "SoHo", "lat": 40.7233, "lon": -73.9985, "weight": 0.04},
        {"zone": "Financial District", "lat": 40.7075, "lon": -74.0089, "weight": 0.06},
        {"zone": "East Village", "lat": 40.7265, "lon": -73.9815, "weight": 0.05},
        {"zone": "Murray Hill", "lat": 40.7485, "lon": -73.9780, "weight": 0.04},
    ]
    dropoff_locations = pickup_locations + [
        {"zone": "Bronx", "lat": 40.8448, "lon": -73.8648, "weight": 0.02},
        {"zone": "Queens", "lat": 40.7282, "lon": -73.7949, "weight": 0.03},
        {"zone": "Staten Island", "lat": 40.5795, "lon": -74.1502, "weight": 0.01},
        {"zone": "Coney Island", "lat": 40.5777, "lon": -73.9716, "weight": 0.02},
        {"zone": "Yankee Stadium", "lat": 40.8296, "lon": -73.9262, "weight": 0.01},
    ]
    airport_zones = {"JFK Airport", "LaGuardia Airport"}
    payment_types = ["Credit Card", "Cash", "Mobile Payment", "Fare Share"]
    payment_weights = [0.55, 0.30, 0.12, 0.03]
    rate_codes = [1, 2, 3, 4, 5]
    surge_hours = {7: 1.3, 8: 1.5, 9: 1.3, 17: 1.4, 18: 1.6, 19: 1.3, 22: 1.2, 23: 1.2}
    weekend_surge = {20: 1.8, 21: 2.0, 22: 1.8, 23: 1.5, 0: 1.3, 1: 1.2}
    out = []
    base_time = datetime(2024, 1, 1)
    pickup_weights = [p["weight"] for p in pickup_locations]
    dropoff_weights = [d["weight"] for d in dropoff_locations]
    for i in range(n):
        pickup_idx = random.choices(range(len(pickup_locations)), weights=pickup_weights, k=1)[0]
        pickup = pickup_locations[pickup_idx]
        dropoff_candidates = list(range(len(dropoff_locations)))
        if pickup_idx < len(pickup_locations):
            dropoff_candidates = [d for d in dropoff_candidates if d != pickup_idx]
        dropoff_idx = random.choices(dropoff_candidates, weights=[dropoff_locations[d]["weight"] for d in dropoff_candidates], k=1)[0]
        dropoff = dropoff_locations[dropoff_idx]
        hour = random.choices(range(24),
            weights=[1,1,1,1,1,2,4,6,8,7,5,4,5,6,7,8,7,6,5,4,3,2,1,1], k=1)[0]
        day_offset = random.randint(0, 365)
        trip_time = base_time + timedelta(days=day_offset, hours=hour, minutes=random.randint(0, 59))
        is_weekend = trip_time.weekday() >= 5
        is_rainy = random.random() < 0.15
        is_rush_hour = hour in [7, 8, 9, 17, 18, 19]
        surge = 1.0
        if is_weekend:
            surge = weekend_surge.get(hour, 1.0)
        elif hour in surge_hours:
            surge = surge_hours[hour]
        if is_rainy:
            surge *= 1.3
        if is_rush_hour:
            surge *= 1.2
        surge = min(surge, 3.0)
        if pickup["zone"] in airport_zones:
            distance = round(random.lognormvariate(2.0, 0.5), 2)
        else:
            distance = round(random.lognormvariate(1.2, 0.6), 2)
        distance = max(0.5, min(distance, 40.0))
        base_speed = 12 if is_rush_hour else 18
        if is_rainy:
            base_speed *= 0.7
        traffic_factor = base_speed / max(1, base_speed + random.gauss(0, 3))
        duration = int(distance / traffic_factor * 60 * 60 + random.randint(60, 300))
        base_fare = 2.50 + distance * 2.50 + duration / 3600 * 0.50
        surge_fare = round(base_fare * surge, 2)
        if is_weekend:
            surge_fare *= 1.1
        tolls = 0
        if distance > 10:
            tolls = random.choice([0, 0, 5.76, 6.55, 8.50, 10.00])
        if dropoff["zone"] in airport_zones:
            tolls = max(tolls, 5.76)
        tip_pct = random.choices([0, 10, 15, 20, 25], weights=[30, 10, 25, 25, 10], k=1)[0]
        if is_rush_hour and random.random() < 0.3:
            tip_pct = min(tip_pct + 5, 30)
        tip = round(surge_fare * tip_pct / 100, 2)
        total = round(surge_fare + tolls + tip, 2)
        if random.random() < 0.02:
            total = round(total * random.uniform(0.1, 0.3), 2)
        payment = random.choices(payment_types, weights=payment_weights, k=1)[0]
        passenger_count = random.choices([1,2,3,4,5,6], weights=[60,20,10,5,3,2], k=1)[0]
        if pickup["zone"] in airport_zones and random.random() < 0.4:
            passenger_count = random.choices([2,3,4], weights=[40,35,25], k=1)[0]
        out.append({
            "id": f"trip_{i:06d}",
            "pickup_zone": pickup["zone"],
            "pickup_lat": pickup["lat"],
            "pickup_lon": pickup["lon"],
            "dropoff_zone": dropoff["zone"],
            "dropoff_lat": dropoff["lat"],
            "dropoff_lon": dropoff["lon"],
            "pickup_time": trip_time.isoformat(),
            "dropoff_time": (trip_time + timedelta(seconds=duration)).isoformat(),
            "distance_miles": distance,
            "duration_seconds": duration,
            "fare_amount": surge_fare,
            "tolls_amount": tolls,
            "tip_amount": tip,
            "total_amount": total,
            "payment_type": payment,
            "rate_code": random.choices(rate_codes, weights=[70,10,10,5,5], k=1)[0],
            "passenger_count": passenger_count,
            "vendor_id": random.choice(["CMT", "VTS"]),
            "surge_multiplier": round(surge, 2),
            "is_rainy": is_rainy,
            "is_rush_hour": is_rush_hour,
            "is_weekend": is_weekend,
            "day_of_week": trip_time.strftime("%A"),
            "hour_of_day": trip_time.hour,
            "airport_trip": pickup["zone"] in airport_zones or dropoff["zone"] in airport_zones,
            "speed_mph": round(distance / max(duration / 3600, 0.01), 1),
        })
    return out

def main():
    data = gen_taxi()
    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / "dataset.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Generated {len(data)} taxi trip records")
    print(f"Saved to {out}")

if __name__ == "__main__":
    main()
