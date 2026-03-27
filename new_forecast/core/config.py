
import pathlib
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

config_path = pathlib.Path(__file__)
base_dir = config_path.parents[1]

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=base_dir.joinpath("settings", ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

class GeocoderConfig(BaseConfig):
    api_key: str
    base_url: str

    model_config = SettingsConfigDict(env_prefix="geocoder_")


class WeatherConfig(BaseConfig):
    api_key: str
    base_url: str

    model_config = SettingsConfigDict(env_prefix="weather_")


class Config(BaseSettings):
    geocoder: GeocoderConfig = Field(default_factory=GeocoderConfig)
    weather: WeatherConfig = Field(default_factory=WeatherConfig)

config = Config()
