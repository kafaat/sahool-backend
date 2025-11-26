from fastapi import APIRouter, HTTPException
from app.modules.weather.services import (
    get_current_weather, get_daily_weather, get_historical_weather
)

router = APIRouter()

@router.get("/current")
def current_weather(lat: float, lon: float):
    try:
        return get_current_weather(lat, lon)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/daily")
def daily_weather(lat: float, lon: float):
    try:
        return get_daily_weather(lat, lon)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/history")
def history_weather(lat: float, lon: float, start: str, end: str):
    try:
        return get_historical_weather(lat, lon, start, end)
    except Exception as e:
        raise HTTPException(500, str(e))
