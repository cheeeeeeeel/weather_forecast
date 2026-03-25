# from geocoder_api.client import GeocoderClient
from weather_api.client import WeatherClient, Coordinates

# geocoder = GeocoderClient()
# with geocoder:
#     coords = geocoder.get_coords("St. Petersburg")
#     # coords_2 = geocoder.get_coords("Санкт-Петербург")
coords = Coordinates(lat=59.938784, lon=30.314997)
print(coords)
with WeatherClient() as weather:
    response = weather._get_data_by_coords(coords)

print(response.json())
# print(coords_2)
# print(coords == coords_2)


# from datetime import datetime
#
# time = datetime.now()
# print(str(time))


