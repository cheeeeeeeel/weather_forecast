# Weather Forecast

## Описание

Данное приложение позволяет получать информацию о текущей погоде в вашем городе или любом другом городе мира. Также ведется история запросов с возможностью просмотра нескольких последних записей.

## Функционал

Приложение получает информацию о погоде с помощью сервиса OpenWeatherMap. Для взаимодействия с этим API необходимо указать город, погода в котором нам интересна. В приложении реализовано два подхода:
1. Вы можете узнать погоду указав название города как на русском, так и на английском. Для этого выберите действие "Погода в указанном городе".
2. При выборе действия "Погода в вашем городе" определяется погода в вашем текущем местоположении. Для этого используется API IPinfo.

Помимо этого вы можете узнать историю запросов в активной сессии при выборе "Истории запросов".

Для завершения работы приложения выберите "Выйти".

Интерфейс для работы с приложением:

````
0 - Выйти
1 - Погода в вашем городе
2 - Погода в указанном городе
3 - История запросов

Выберите действие (4 - меню команд):
````

Формат ответа:
````
Текущее время: 2025-01-05 04:21:53+03:00
Название города: Санкт-Петербург
Погодные условия: облачно с прояснениями
Текущая температура: -6 градусов по цельсию
Ощущается как: -10 градусов по цельсию
Скорость ветра: 3 м/c
````

## Запуск

Для запуска приложения необходимо:

1. Скопировать репозиторий на свой компьютер.

```
git clone https://github.com/cheeeeeeeel/weather_forecast
```

2. Установить зависимости.

```
pip install -r requirements.txt
```

3. Создайте файл с названием ".env" в директории проекта. В нём создайте константу с названием "OpenWeatherMap_KEY" 
и присвойте ей значение вашего API ключа, который вы можете получить на [сайте сервиса](https://openweathermap.org/api) после регистрации.

```
OpenWeatherMap_KEY = "ваш ключ для API"
```

4. И наконец запустить приложение.

```
python -m forecast
```

### Приятного использования!
