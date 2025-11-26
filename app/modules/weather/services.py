import requests

BASE_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

def get_current_weather(lat: float, lon: float):
    params = {
        "latitude": lat, "longitude": lon,
        "current": [
            "temperature_2m","relative_humidity_2m",
            "wind_speed_10m","wind_direction_10m",
            "surface_pressure","precipitation"
        ],
    }
    r = requests.get(BASE_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("current", {})

def get_daily_weather(lat: float, lon: float):
    params = {
        "latitude": lat, "longitude": lon,
        "daily": [
            "temperature_2m_max","temperature_2m_min",
            "precipitation_sum","wind_speed_10m_max"
        ]
    }
    r = requests.get(BASE_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("daily", {})

def get_historical_weather(lat: float, lon: float, start: str, end: str):
    params = {
        "latitude": lat, "longitude": lon,
        "start_date": start, "end_date": end,
        "daily": [
            "temperature_2m_max","temperature_2m_min",
            "precipitation_sum","wind_speed_10m_max"
        ]
    }
    r = requests.get(ARCHIVE_URL, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("daily", {})
