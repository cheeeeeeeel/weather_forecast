
import requests
from datetime import datetime

from .config import API_KEY, API_BASE_URL
from weather_forecast.models import WeatherData, Coordinates
from weather_forecast.exceptions import InvalidApiResponseError
from weather_forecast.geocoder_api.client import HttpRequest
from requests.models import Response


LANG = "ru"

class WeatherClient:
    def __init__(self, session: requests.Session | None = None, timeout=10):
        self._key = API_KEY
        self._base_url = API_BASE_URL
        self._request = HttpRequest()
        self._own_session_flag = session is None
        self._session = session or requests.Session()
        self._timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._own_session_flag:
            self._session.close()

    def _get_data_by_coords(self, coords) -> Response | None:
        """Принимет не название города, а ширину и долготу"""
        payload = {
            "lat": coords.lat,
            "lon": coords.lon,
            "key": self._key,
            "lang": LANG,
        }
        response = self._request.get(self._base_url, params=payload, timeout=self._timeout)
        return response

    def _validate_response(self, response) -> dict:
        try:
            response = response.json()
            if "data" not in response:
                raise InvalidApiResponseError("Некорректная структура ответа от АПИ погоды.")
            return response
        except ValueError as e:
            raise InvalidApiResponseError("Формат ответа от АПИ погоды не соответствует ожидаемому.") from e

    def _parser(self, data):
        try:
            time = datetime.time
        except (LookupError, TypeError) as e:
            raise InvalidApiResponseError(
                f"Ошибка в парсинге координат. Возможно структура ответа обрабатывается некорректо или изменилась. \n {e}"
            ) from e

    def get_weather_data(self, coords: Coordinates) -> WeatherData:
        response = self._get_data_by_coords(coords)
        data = self._validate_response(response)
        return self._parser(data)




























