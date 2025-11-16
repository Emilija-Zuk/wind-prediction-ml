"""Configuration for weather data processing."""

# Weather stations with their IDs
STATIONS = [
    ["GC", "18591"], 
    ["COOLLY", "18118"], 
    ["HOPE", "39817"],
    ["BANANA", "39818"], 
    ["CAPE", "30280"], 
    ["BYRON_MAIN", "19017"]
]

# Data paths
RAW_DATA_DIR = "../data-raw/full"
PROCESSED_DATA_DIR = "../data-processed/base"
ENHANCED_DATA_DIR = "../data-processed/enhanced"

# Observational data field keys
OBSERVATIONAL_KEYS = [
    "wind", "pressure", "wind-gust", "rainfall", "temperature",
    "apparent-temperature", "cloud", "delta-t", "dew-point", "humidity"
]

# Expected fields per station (for handling missing data)
STATION_FIELDS = [
    "wind", "wind_direction", "pressure", "wind_gust", "rain", 
    "temp", "apparent_temp", "cloud_oktas", "delta_t", "dew_point", 
    "humidity", "wind_dir_cos", "wind_dir_sin"
]

# Forecast fields
FORECAST_FIELDS = [
    "GC_forecast_wind",
    "GC_forecast_direction", 
    "GC_forecast_direction_cos",
    "GC_forecast_direction_sin"
]

# Brisbane timezone offset (UTC+10)
BRISBANE_UTC_OFFSET = 36000  # seconds

# Gold Coast coordinates for sunrise/sunset calculations
GOLD_COAST_LAT = -28.0167
GOLD_COAST_LON = 153.4000
TIMEZONE = "Australia/Brisbane"
