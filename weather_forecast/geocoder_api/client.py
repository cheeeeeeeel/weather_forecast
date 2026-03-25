import random
import time
import requests

from weather_forecast.models import Coordinates
from weather_forecast.exceptions import InvalidApiResponseError, NetworkError, RequestError
from .config import API_KEY, API_BASE_URL
from requests import Response



class HttpRequest:

    def __init__(self, max_retries: int, delay: int):
        self._max_retries = max_retries
        self._delay = delay

    def get(self, *args, **kwargs) -> Response | None:
        for attempt in range(1, self._max_retries + 1):
            try:
                response = requests.get(*args, **kwargs)
                response.raise_for_status()
                return response

            except requests.HTTPError as e:
                if e.response.status_code < 500:
                    raise RequestError(f"Клиентская ошибка: {e}") from e
                if attempt == self._max_retries:
                    raise RequestError(f"Ошибка на сервере АПИ: {e}") from e

            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt == self._max_retries:
                    raise NetworkError(
                        f"Ошибка сети: {e}"
                    ) from e
            sleep = self._delay * (2 ** (attempt - 1)) + random.uniform(0.1, 0.4)
            time.sleep(sleep)

LANG = "ru_RU"
FORMAT = "json"

class GeocoderClient:

    def __init__(self, session: requests.Session | None = None,
                 max_retries: int = 3, delay: int = 3, timeout: int = 10):
        self._base_url = API_BASE_URL
        self._key = API_KEY
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

    def _get(self, city: str) -> Response | None:
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
