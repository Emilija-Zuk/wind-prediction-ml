"""Process weather data for a single date."""

import json
import os
import sys
from datetime import datetime

import pandas as pd

from config import STATIONS, PROCESSED_DATA_DIR, ENHANCED_DATA_DIR
from processors import load_station_data, load_forecast_data, merge_timelines
from enhancement import enhance_features


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
    
    # Convert to DataFrame
    df_base = pd.DataFrame(merged_data)
    
    # Save base outputs
    save_base_outputs(df_base, date)
    
    # Enhance features in-memory
    df_enhanced = enhance_features(df_base, date)
    
    # Save enhanced outputs
    save_enhanced_outputs(df_enhanced, date)
    
    print(f"Completed processing for {date}")


def save_base_outputs(df: pd.DataFrame, date: str) -> None:
    """
    Save base processed data to JSON and Parquet files.
    
    Args:
        df: Base DataFrame with merged data
        date: Date string for filename
    """
    # Ensure output directory exists
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    # Save JSON
    json_path = f"{PROCESSED_DATA_DIR}/full_data_{date}.json"
    data = df.to_dict('records')
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved base JSON: {json_path}")
    
    # Save Parquet
    parquet_path = f"{PROCESSED_DATA_DIR}/full_data_{date}.parquet"
    df.to_parquet(parquet_path, index=False)
    print(f"Saved base Parquet: {parquet_path}")


def save_enhanced_outputs(df: pd.DataFrame, date: str) -> None:
    """
    Save enhanced data to JSON and Parquet files.
    
    Args:
        df: Enhanced DataFrame with additional features
        date: Date string for filename
    """
    # Ensure output directory exists
    os.makedirs(ENHANCED_DATA_DIR, exist_ok=True)
    
    # Save JSON
    json_path = f"{ENHANCED_DATA_DIR}/full_data_{date}.json"
    data = df.to_dict('records')
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved enhanced JSON: {json_path}")
    
    # Save Parquet
    parquet_path = f"{ENHANCED_DATA_DIR}/full_data_{date}.parquet"
    df.to_parquet(parquet_path, index=False)
    print(f"Saved enhanced Parquet: {parquet_path}")



def main():
    """Main entry point."""
    date = "2025-11-15"
    process_date(date)


if __name__ == "__main__":
    main()
