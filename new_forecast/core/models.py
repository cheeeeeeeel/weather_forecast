from datetime import datetime
from dataclasses import dataclass

@dataclass
class WeatherData:
    time: datetime
    city: str
    weather_condition: str
    temperature: int
    temp_feels_like: int
    wind_speed: int


@dataclass
class Coordinates:
    lat: float
    lon: float

