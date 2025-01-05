import requests
from enum import Enum
from collections import namedtuple
from datetime import datetime, timedelta, timezone


class Actions(Enum):

    show_menu = 4
    get_history = 3
    get_forecast_by_city = 2
    get_forecast_by_ip = 1
    close_app = 0

WeatherData = namedtuple("WeatherData", "time name conditions temperature feels_like wind")

class Storage:

    history = []
    query_count = 0

    @classmethod
    def add_forecast(cls, forecast: WeatherData) -> None:
        cls.history.append(forecast)
        cls.query_count += 1

    @classmethod
    def show_last_n_queries(cls) -> None:
        if cls.query_count == 0:
            return print("История пуста")
        while True:
            try:
                n = int(input(f"Число записей в истории: {cls.query_count}. \n"
                              f"Сколько последних записей вы хотите видеть: "))
                if n <= 0 or n > cls.query_count:
                    raise IndexError
            except ValueError:
                print("Поле ввода должно содержать только цифры!")
            except IndexError:
                print(
                    "Указанное вами число превосходит количество записей в истории \n"
                    "или не является положительным."
                )
            else:
                for query in cls.history[-n::]:
                    print_weather_info(query)
                break


def main() -> None:
    menu()
    while True:
        action = choose_action()
        if action == Actions.close_app.value:
            break


def menu() -> None:
    print(f"""
        {Actions.close_app.value} - Выйти
        {Actions.get_forecast_by_ip.value} - Погода в вашем городе
        {Actions.get_forecast_by_city.value} - Погода в указанном городе
        {Actions.get_history.value} - История запросов""")


def choose_action() -> int | None:
    try:
        status = int(input(f"Выберите действие ({Actions.show_menu.value} - меню команд): "))
    except ValueError:
        print("Поле ввода должно содержать только цифры!")
    else:
        if status == Actions.close_app.value:
            print("До свидания!")
            return Actions.close_app.value

        elif status == Actions.get_forecast_by_ip.value:
            get_forecast(get_ip_location())

        elif status == Actions.get_forecast_by_city.value:
            get_forecast(get_city_name())

        elif status == Actions.get_history.value:
            Storage.show_last_n_queries()

        elif status == Actions.show_menu.value:
            menu()

        else:
            print(f"Команды с номером {status} не существует.")


def get_ip_location() -> str:
    response = requests.get("http://ipinfo.io/json").json()
    return response["city"]


def get_city_name() -> str:
    return input("Введите название города: ")


def get_forecast(city_name: str) -> None:
    try:
        weather_data = get_weather_data(city_name)
        print_weather_info(weather_data)
    except KeyError:
        print("Город с таким названием не найден.")
    except Exception as e:
        print(f"Случилось что-то неладное: {e}.")


def get_weather_data(city_name: str) -> WeatherData:
    params = {
        "q": city_name,
        "APPID": "158a57a9df031a35e520c959cd1607d1",
        "units": "metric",
        "lang": "ru"
    }
    response = requests.post("https://api.openweathermap.org/data/2.5/weather", params=params).json()
    data = WeatherData(
        time=get_current_time(response["timezone"]),
        name=response["name"],
        conditions=response["weather"][0]["description"],
        temperature=round(response["main"]["temp"]),
        feels_like=round(response["main"]["feels_like"]),
        wind=round(response["wind"]["speed"]),
    )
    Storage.add_forecast(data)
    return data


def get_current_time(shift: int) -> str:
    date = datetime.now(tz=timezone(timedelta(seconds=shift))).strftime("%Y-%m-%d %H:%M:%S%Z")
    return date.replace("UTC", "")


def print_weather_info(weather: WeatherData) -> None:
    print(f"""
    Текущее время: {weather.time}
    Название города: {weather.name}
    Погодные условия: {weather.conditions}
    Текущая температура: {weather.temperature} градусов по цельсию
    Ощущается как: {weather.feels_like} градусов по цельсию
    Скорость ветра: {weather.wind} м/c""")


if __name__ == "__main__":
    main()

