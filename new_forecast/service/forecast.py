
from datetime import datetime
from dateutil import tz
from new_forecast.core.models import ForecastData
import new_forecast.clients as clients


class Forecast:

    def __init__(self, geocoder: clients.GeocoderClient,
                 weather: clients.WeatherClient,
                 translator: clients.Translator):
        self._geocoder = geocoder
        self._weather = weather
        self._translator = translator

    def get_forecast_data(self, city) -> ForecastData:
        coords = self._geocoder.get_coords(city)
        tz_iana, city_en, *weather_data = self._weather.get_weather_data(coords)
        forecast = ForecastData(
            self._get_current_time(tz_iana),
            self._translator.translate(city_en),
            *weather_data
        )
        return forecast

    def _get_current_time(self, tz_iana: str) -> datetime:
        time_zone = tz.gettz(tz_iana)
        now = datetime.now(tz=time_zone)
        return now