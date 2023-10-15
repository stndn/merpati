# Application configuration

import os
from time import localtime, strftime

class Config(object):
  DEBUG = False
  TESTING = False
  app_version = "v1"
  APP_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
  locations_file = os.path.abspath(os.path.join(APP_PATH, 'config/locations.json'))

  open_meteo_weather_url = ("https://api.open-meteo.com/v1/forecast?"
                            "latitude={lat}&longitude={long}&"
                            "current=temperature_2m,relativehumidity_2m,"
                            "apparent_temperature,precipitation,weathercode,"
                            "windspeed_10m,winddirection_10m,is_day&"
                            "hourly=temperature_2m,relativehumidity_2m,"
                            "apparent_temperature,precipitation_probability,"
                            "precipitation,weathercode,windspeed_10m,"
                            "winddirection_10m,is_day&"
                            "timezone=auto&forecast_days=3"
                           )

  output_path   = os.path.abspath(os.path.join(APP_PATH, 'output/'))
  archive_path  = os.path.abspath(os.path.join(APP_PATH, 'archive/'))

  outfile_suffix = strftime("%Y%m%dT%H%M%S", localtime())


class Development(Config):
  DEBUG = True

class Production(Config):
  DEBUG = False

class Testing(Config):
  DEBUG = False
  TESTING=True

