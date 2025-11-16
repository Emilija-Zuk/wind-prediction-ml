"""Convert parquet file back to JSON for testing/verification."""

import json
import pandas as pd


def parquet_to_json():
    """Load parquet file and convert to JSON."""
    date = "2025-11-15"
    
    # Read parquet file
    parquet_path = f"../data-processed/base/full_data_{date}.parquet"

    df = pd.read_parquet(parquet_path)
    
    # Convert to list of dicts
    data = df.to_dict('records')
    
    # Save as JSON
    json_path = f"../data-processed/base/full_data_{date}_converted.json"
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved: {json_path}")
  


if __name__ == "__main__":
    parquet_to_json()
