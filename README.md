# 🌬️ Wind Prediction ML


> **Machine learning and data layer for short-range wind forecasting around the Gold Coast, Queensland**

A specialized ML pipeline designed to predict wind patterns with 10-minute resolution over the next 3 hours, leveraging real-time weather station data from the WillyWeather API.

## 🎯 Overview

This repository handles the data for wind prediction:

- **🔄 Data Processing**: Transforms raw weather observations into ML-ready features
- **🤖 Model Training**: Implements time-series forecasting models for wind prediction
- **⚡ Real-time Pipeline**: Processes live data from multiple Gold Coast weather stations

## 📡 Data Sources

### Weather Stations
- **GC** (Gold Coast) - Primary station
- **BANANA** (Banana Island)
- **BYRON_MAIN** (Byron Bay Main)
- **CAPE** (Cape Byron)
- **COOLLY** (Coolangatta)
- **HOPE** (Hope Island)

### Meteorological Variables

| Variable | Unit | Description |
|----------|------|-------------|
| Wind Speed | km/h | 10-minute average wind speed |
| Wind Direction | degrees | Wind direction (0-359°) |
| Wind Gust | km/h | Maximum gust in 10-min period |
| Pressure | hPa | Atmospheric pressure |
| Temperature | °C | Air temperature |
| Apparent Temperature | °C | Feels-like temperature |
| Rainfall | mm | Precipitation in 10-min period |
| Humidity | % | Relative humidity |
| Dew Point | °C | Dew point temperature |
| Cloud Cover | oktas | Cloud coverage (0-8 scale) |
| Delta-T | °C | Temperature stability indicator |

### Feature Engineering

**Circular Encoding for Wind Direction:**
```python
wind_dir_cos = cos(wind_direction * π / 180)
wind_dir_sin = sin(wind_direction * π / 180)
```

*All timestamps are in Brisbane local time, synchronized to 10-minute intervals.*


<p align="center">
  <strong>🌊 Built for accurate coastal wind forecasting in Queensland</strong>
</p>