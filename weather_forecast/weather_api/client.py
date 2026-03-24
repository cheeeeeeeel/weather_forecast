
from config import API_KEY, API_BASE_URL
from weather_forecast.models import WeatherData
import requests

class WeatherClient:
    def __init__(self):
        self.key = API_KEY
        self.url = API_BASE_URL

    def _get_json_data(self, lat, lon):
        """Принимет не название города, а ширину и долготу"""
        payload = {
            "lat": lat,
            "lon": lon,
            "key": self.key,
            "lang": "ru",
        }
        r = requests.get(self.url, params=payload)
        r.raise_for_status()
        return r.json()


    def _parser(self, data) -> WeatherData:
        pass

    def get_weather_data(self, lat, lon) -> WeatherData:
        json_data = self._get_json_data(lat,lon)
        return self._parser(json_data)

    