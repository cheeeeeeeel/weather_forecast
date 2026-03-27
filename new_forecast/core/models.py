from datetime import datetime
from dataclasses import dataclass

@dataclass
class WeatherData:
    tz_iana: str
    city_en: str
    weather_condition: str
    temperature: float
    temp_feels_like: float
    wind_speed: float


@dataclass
class Coordinates:
    lat: float
    lon: float


@dataclass
class ForecastData:
    time: datetime
    city: str
    weather_condition: str
    temperature: int
    temp_feels_like: int
    wind_speed: int