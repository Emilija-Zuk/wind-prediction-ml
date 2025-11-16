"""Data processing functions for weather station data."""

import json
import math
import os
from datetime import datetime
from typing import Dict, Tuple, List

from config import (
    STATIONS, RAW_DATA_DIR, OBSERVATIONAL_KEYS, 
    STATION_FIELDS, FORECAST_FIELDS, BRISBANE_UTC_OFFSET
)


def load_station_data(station_name: str, station_id: str, date: str) -> Dict[int, Dict]:
    """
    Load observational data for a single station.
    
    Args:
        station_name: Name of the station (e.g., "GC")
        station_id: Station ID (e.g., "18591")
        date: Date string in format "YYYY-MM-DD"
    
    Returns:
        Dictionary mapping timestamp to data entry with station-prefixed fields
    """
    in_path = f"{RAW_DATA_DIR}/{station_name}{date}.json"
    
    if not os.path.exists(in_path):
        print(f"Warning: File not found for {station_name}: {in_path}")
        return {}
    
    with open(in_path) as f:
        d = json.load(f)

    def points(name):
        return d["observationalGraphs"][name]["dataConfig"]["series"]["groups"][0]["points"]

    # Extract all data series
    series = {}
    for k in OBSERVATIONAL_KEYS:
        series[k] = points(k)

    # Build timestamp-indexed data map
    data_map = {}
    for k, lst in series.items():
        for p in lst:
            t = p["x"]
            e = data_map.setdefault(t, {"timestamp": t})

            match k:
                case "wind":
                    e[f"{station_name}_wind"] = p.get("y")
                    e[f"{station_name}_wind_direction"] = p.get("direction")
                case "pressure":
                    e[f"{station_name}_pressure"] = p.get("y")
                case "wind-gust":
                    e[f"{station_name}_wind_gust"] = p.get("y")
                case "rainfall":
                    e[f"{station_name}_rain"] = p.get("y")
                case "temperature":
                    e[f"{station_name}_temp"] = p.get("y")
                case "apparent-temperature":
                    e[f"{station_name}_apparent_temp"] = p.get("y")
                case "cloud":
                    e[f"{station_name}_cloud_oktas"] = p.get("y")
                case "delta-t":
                    e[f"{station_name}_delta_t"] = p.get("y")
                case "dew-point":
                    e[f"{station_name}_dew_point"] = p.get("y")
                case "humidity":
                    e[f"{station_name}_humidity"] = p.get("y")

    # Calculate wind direction components
    calculate_wind_components(data_map, station_name)
    
    return data_map


def load_forecast_data(date: str) -> Dict[int, Dict]:
    """
    Load forecast data for a given date.
    
    Args:
        date: Date string in format "YYYY-MM-DD"
    
    Returns:
        Dictionary mapping timestamp to forecast data with GC_forecast_* fields
    """
    forecast_path = f"{RAW_DATA_DIR}/FORECAST{date}.json"
    forecast_data_map = {}

    if not os.path.exists(forecast_path):
        print(f"Warning: Forecast file not found: {forecast_path}")
        return forecast_data_map

    print(f"Loading forecast data from {forecast_path}...")
    with open(forecast_path) as f:
        forecast_json = json.load(f)
    
    # Extract forecast entries for the target date only (first day)
    if "forecasts" in forecast_json and "wind" in forecast_json["forecasts"]:
        days = forecast_json["forecasts"]["wind"]["days"]
        if days and len(days) > 0:
            entries = days[0]["entries"]
            
            for entry in entries:
                # Parse datetime string - it's in Brisbane time (UTC+10)
                dt_str = entry["dateTime"]  # e.g., "2025-11-15 00:00:00"
                dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                # dt.timestamp() interprets as UTC, but we need Brisbane time (UTC+10)
                # Add 10 hours (36000 seconds) to correct the offset
                timestamp = int(dt.timestamp()) + BRISBANE_UTC_OFFSET
                
                # Store forecast data
                forecast_data_map[timestamp] = {
                    "GC_forecast_wind": entry["speed"],
                    "GC_forecast_direction": entry["direction"]
                }
                
                # Calculate cos/sin for direction
                deg = entry["direction"]
                if deg is not None:
                    rad = deg * math.pi / 180.0
                    forecast_data_map[timestamp]["GC_forecast_direction_cos"] = math.cos(rad)
                    forecast_data_map[timestamp]["GC_forecast_direction_sin"] = math.sin(rad)
    
    print(f"Loaded {len(forecast_data_map)} forecast entries")
    return forecast_data_map


def calculate_wind_components(data_map: Dict[int, Dict], station_name: str) -> None:
    """
    Calculate cos/sin components for wind direction.
    Modifies data_map in place.
    
    Args:
        data_map: Dictionary mapping timestamp to data entries
        station_name: Name of the station for field prefixing
    """
    for t, e in data_map.items():
        deg = e.get(f"{station_name}_wind_direction")
        if deg is not None:
            rad = deg * math.pi / 180.0
            e[f"{station_name}_wind_dir_cos"] = math.cos(rad)
            e[f"{station_name}_wind_dir_sin"] = math.sin(rad)


def merge_timelines(
    station_data_maps: Dict[str, Dict[int, Dict]], 
    forecast_data_map: Dict[int, Dict],
    master_station: str = "GC"
) -> List[Dict]:
    """
    Merge all station data and forecast data using master station timeline.
    
    Args:
        station_data_maps: Dictionary of station_name -> timestamp -> data
        forecast_data_map: Dictionary of timestamp -> forecast data
        master_station: Station to use as master timeline (default: "GC")
    
    Returns:
        List of merged data entries sorted by timestamp
    """
    if master_station not in station_data_maps:
        raise Exception(f"{master_station} station data not found - cannot proceed without master timeline")

    merged_data_map = {}
    for timestamp in sorted(station_data_maps[master_station].keys()):
        merged_entry = {"timestamp": timestamp}
        
        # Add data from all stations for this timestamp
        for station_name, station_id in STATIONS:
            if station_name in station_data_maps:
                station_entry = station_data_maps[station_name].get(timestamp, {})
                # Copy all station-specific fields
                for key, value in station_entry.items():
                    if key != "timestamp":
                        merged_entry[key] = value
            else:
                # Station not available - add None for all expected fields
                for field in STATION_FIELDS:
                    merged_entry[f"{station_name}_{field}"] = None
        
        # Add forecast data if available for this timestamp
        if timestamp in forecast_data_map:
            for key, value in forecast_data_map[timestamp].items():
                merged_entry[key] = value
        else:
            # No forecast for this timestamp - add None
            for field in FORECAST_FIELDS:
                merged_entry[field] = None
        
        merged_data_map[timestamp] = merged_entry

    # Return as sorted list
    return [merged_data_map[t] for t in sorted(merged_data_map.keys())]
