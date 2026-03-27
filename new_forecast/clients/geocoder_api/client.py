
import requests

from new_forecast.core import (
config,
HttpRequest,
InvalidApiResponseError,
Coordinates
)
from requests import Response


LANG = "ru_RU"
FORMAT = "json"

class GeocoderClient:

    def __init__(self, session: requests.Session | None = None,
                 max_retries: int = 3, delay: float = 3, timeout: int = 10):
        self._base_url = config.geocoder.base_url
        self._key = config.geocoder.api_key
        self._own_session_flag = session is None
        self._session = session or requests.Session()
        self._request = HttpRequest(max_retries, delay)
        self._timeout = timeout

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._own_session_flag:
            self._session.close()

    def get_coords(self, city: str) -> Coordinates:
        response = self._get(city)
        data = self._validate_response(response)
        return self._parse_coords(data)

    def _get(self, city: str) -> Response:
        payload = {
            "apikey": self._key,
            "geocode": city,
            "lang": LANG,
            "format": FORMAT,
        }
        response = self._request.get(self._base_url, params=payload, timeout=self._timeout)
        return response

    def _validate_response(self, response: Response) -> dict:
        try:
            data = response.json()
            if "response" not in data:
                raise InvalidApiResponseError(f"Некорректная структура ответа от Геокодер.")
        except ValueError as e:
            raise InvalidApiResponseError(f"Некорректный формат ответ от Геокодера. \n {e}") from e
        return data

    def _parse_coords(self, data: dict) -> Coordinates:
        try:
            coords: str = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
            lon, lat = coords.split()
            return Coordinates(float(lat), float(lon))
        except (LookupError, TypeError) as e:
            raise InvalidApiResponseError(
                f"Ошибка в парсинге координат. Возможно структура ответа обрабатывается некорректо или изменилась. \n {e}"
            ) from e
