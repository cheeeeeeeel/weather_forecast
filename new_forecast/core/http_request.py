
import random
import time
import requests
from requests import Response
from new_forecast.core import RequestError, NetworkError

class HttpRequest:

    def __init__(self, max_retries: int, delay: float):
        self._max_retries = max_retries if max_retries > 1 else 1
        self._delay = delay if delay > 1 else 1

    def get(self, *args, **kwargs) -> Response:
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
