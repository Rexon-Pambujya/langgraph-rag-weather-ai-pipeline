import requests
from datetime import datetime, timezone, timedelta
from src.config import Config

BASE_URL = Config.BASE_URL
API_KEY = Config.API_KEY
DEFAULT_CITY = Config.DEFAULT_CITY

def fetch_weather_by_city(city: str = DEFAULT_CITY, units:str=Config.UNITS) -> dict:
    params = {
        'q': city,
        'appid': API_KEY,
        'units': units,
        'lang': Config.LANGUAGE
    }
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    # canonicalize a small result structure
    dt_unix = data.get('dt')
    tz_offset = data.get('timezone', 0) or 0
    obs_time_local = None
    if isinstance(dt_unix, (int, float)):
        obs_time_utc = datetime.fromtimestamp(dt_unix, tz=timezone.utc)
        obs_time_local = obs_time_utc + timedelta(seconds=tz_offset)

    result = {
        'city': data.get('name'),
        'country': data.get('sys', {}).get('country'),
        'temperature': data.get('main', {}).get('temp'),
        'description': data.get('weather', [{}])[0].get('description'),
        'humidity': data.get('main', {}).get('humidity'),
        'wind_speed': data.get('wind', {}).get('speed'),
        'observation_time': obs_time_local.isoformat() if obs_time_local else None,
        'raw': data,
    }

    return result