import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def validate_and_ingest(file_path=None):
    dataset_path = DATA_DIR / "dataset.json"
    if not dataset_path.exists():
        print(f"No dataset found at {dataset_path}. Run generate.py first.")
        return False
    with open(dataset_path) as f:
        data = json.load(f)
    required_fields = ["id", "pickup_zone", "dropoff_zone", "fare_amount", "total_amount"]
    for i, record in enumerate(data):
        for field in required_fields:
            if field not in record:
                print(f"Record {i} missing field: {field}")
                return False
        if record["fare_amount"] < 0 or record["total_amount"] < 0:
            print(f"Record {i} has negative fare/total")
            return False
    print(f"Validated {len(data)} records. Dataset is ready.")
    return True

if __name__ == '__main__':
    validate_and_ingest()
