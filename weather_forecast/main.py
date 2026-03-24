from geocoder_api.client import GeocoderClient


geocoder = GeocoderClient()
with geocoder:
    coords = geocoder.get_coords("Санкт-Петербург")

print(coords)
