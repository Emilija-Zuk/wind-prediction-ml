"""Feature enhancement functions for weather data."""

from datetime import datetime, timezone
import pandas as pd
from astral import LocationInfo
from astral.sun import sun

from config import GOLD_COAST_LAT, GOLD_COAST_LON, TIMEZONE


def add_hour(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add hour field (0-23) extracted from timestamp.
    
    Args:
        df: DataFrame with 'timestamp' column (Unix timestamp in Brisbane time)
    
    Returns:
        DataFrame with added 'hour' column
    """
    df = df.copy()
    # Timestamps are already in Brisbane time, just convert directly and extract hour
    df['hour'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour
    return df


def add_daylight(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """
    Add daylight boolean field based on sunrise/sunset times.
    
    Args:
        df: DataFrame with 'timestamp' column (Unix timestamp in Brisbane time)
        date: Date string in format "YYYY-MM-DD"
    
    Returns:
        DataFrame with added 'daylight' column (True if between sunrise and sunset)
    """
    df = df.copy()
    
    # Parse date
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Create location info for Gold Coast
    location = LocationInfo(
        name="Gold Coast",
        region="Australia",
        timezone=TIMEZONE,
        latitude=GOLD_COAST_LAT,
        longitude=GOLD_COAST_LON
    )
    
    # Calculate sunrise and sunset for this date
    s = sun(location.observer, date=date_obj, tzinfo=TIMEZONE)
    sunrise_time = s['sunrise']
    sunset_time = s['sunset']
    
    # These timestamps from astral are in UTC, but my timestamps are in Brisbane time
    # add the Brisbane offset (UTC+10) to make them comparable
    from config import BRISBANE_UTC_OFFSET
    sunrise_ts = int(sunrise_time.timestamp()) + BRISBANE_UTC_OFFSET
    sunset_ts = int(sunset_time.timestamp()) + BRISBANE_UTC_OFFSET
    
    print(f"Sunrise: {sunrise_time.strftime('%H:%M:%S')} (timestamp: {sunrise_ts})")
    print(f"Sunset: {sunset_time.strftime('%H:%M:%S')} (timestamp: {sunset_ts})")
    
    # check if each timestamp is during daylight
    df['daylight'] = (df['timestamp'] >= sunrise_ts) & (df['timestamp'] <= sunset_ts)
    
    return df


def enhance_features(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """
    Enhance weather data with additional features.
    
    Args:
        df: Base weather data DataFrame
        date: Date string for sunrise/sunset calculation
    
    Returns:
        Enhanced DataFrame with hour and daylight fields
    """
    print(f"Enhancing features for {date}...")
    
    df = add_hour(df)
    
    df = add_daylight(df, date)
    
    print(f"Added features: hour, daylight")
    
    return df
