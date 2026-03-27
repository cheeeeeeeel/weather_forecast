# from geocoder_api.client import GeocoderClient
# from weather_api.client import WeatherClient
#
#
#
# if __name__ == "__main__":
#     geocoder = GeocoderClient()
#     with geocoder:
#         coords = geocoder.get_coords("St. Petersburg")
#         # coords_2 = geocoder.get_coords("Санкт-Петербург")
#
#     print(coords)
#     with WeatherClient() as weather:
#         response = weather._get_data_by_coords(coords)
#
#     print(response.json())
#     # print(coords_2)
#     # print(coords == coords_2)
#
#
#     # from datetime import datetime
#     #
#     # time = datetime.now()
#     # print(str(time))
#
#


from core.config import config

print(config.geocoder.base_url)