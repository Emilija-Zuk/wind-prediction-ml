"""Process weather data for a single date."""

import json
import os
import sys
from datetime import datetime

import pandas as pd

from config import STATIONS, PROCESSED_DATA_DIR
from processors import load_station_data, load_forecast_data, merge_timelines


def process_date(date: str) -> None:
    """
    Process weather data for a single date.
    
    Args:
        date: Date string in format "YYYY-MM-DD"
    """
    print(f"Processing data for {date}...")
    
    # Load all station data
    station_data_maps = {}
    for station_name, station_id in STATIONS:
        data_map = load_station_data(station_name, station_id, date)
        if data_map:  # Only add if data was loaded
            station_data_maps[station_name] = data_map
    
    # Load forecast data
    forecast_data_map = load_forecast_data(date)
    
    # Merge all timelines
    merged_data = merge_timelines(station_data_maps, forecast_data_map)
    
    # Save outputs
    save_outputs(merged_data, date)
    
    print(f"Completed processing for {date}")


def save_outputs(data: list, date: str) -> None:
    """
    Save processed data to JSON and Parquet files.
    
    Args:
        data: List of merged data entries
        date: Date string for filename
    """
    # Ensure output directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    # Save JSON
    json_path = f"{PROCESSED_DATA_DIR}/full_data_{date}.json"
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved: {json_path}")
    
    # Save Parquet
    df = pd.DataFrame(data)
    parquet_path = f"{PROCESSED_DATA_DIR}/full_data_{date}.parquet"
    df.to_parquet(parquet_path, index=False)
    print(f"Saved: {parquet_path}")


def main():
    """Main entry point."""
    date = "2025-11-15"
    process_date(date)


if __name__ == "__main__":
    main()
