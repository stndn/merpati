import os
import json
import pandas as pd
import numpy as np
from libs import configurator
from libs import helper
from minio import Minio
from minio.commonconfig import Tags


def get_weather_header(data:json) -> dict:
  grouped_data = {'uuid':                   data['uuid'],
                  'location_name':          data['location_name'],
                  'location_country':       data['location_country'],
                  'location_latitude':      data['location_latitude'],
                  'location_longitude':     data['location_longitude'],
                  'latitude':               data['latitude'],
                  'longitude':              data['longitude'],
                  'utc_offset_seconds':     data['utc_offset_seconds'],
                  'timezone':               data['timezone'],
                  'timezone_abbreviation':  data['timezone_abbreviation'],
                  'elevation' :             data['elevation'],
                  'data_timestamp':         data['current_weather']['time'],
                 }
  return pd.json_normalize(grouped_data)


def get_weather_units(data:json) -> dict:
  grouped_data = {'uuid':                   data['uuid'],
                  'location_name':          data['location_name'],
                  'location_country':       data['location_country'],
                  'location_latitude':      data['location_latitude'],
                  'location_longitude':     data['location_longitude'],
                  'latitude':               data['latitude'],
                  'longitude':              data['longitude'],
                  'current_weather_units':  data['current_weather_units'],
                  'hourly_units':           data['hourly_units'],
                  'data_timestamp':         data['current_weather']['time'],
                 }
  return pd.json_normalize(grouped_data)


def get_weather_current(data:json) -> dict:
  grouped_data = {'uuid':                   data['uuid'],
                  'location_name':          data['location_name'],
                  'location_country':       data['location_country'],
                  'location_latitude':      data['location_latitude'],
                  'location_longitude':     data['location_longitude'],
                  'latitude':               data['latitude'],
                  'longitude':              data['longitude'],
                  'data_timestamp':         data['current_weather']['time'],
                 }
  for k, v in data['current_weather'].items():
    grouped_data[k] = v
  return pd.json_normalize(grouped_data)


def get_weather_hourly(data:json) -> dict:
  grouped_data = {'uuid':                   data['uuid'],
                  'location_name':          data['location_name'],
                  'location_country':       data['location_country'],
                  'location_latitude':      data['location_latitude'],
                  'location_longitude':     data['location_longitude'],
                  'latitude':               data['latitude'],
                  'longitude':              data['longitude'],
                  'data_timestamp':         data['current_weather']['time'],
                 }
  for k, v in data['hourly'].items():
    grouped_data[k] = v
  return pd.DataFrame(grouped_data)


if __name__ == '__main__':

  # Initialize all configurations
  cfg = configurator.init_config()
  log = configurator.init_logger(name='parse_weather',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )
  minio_cfg = configurator.init_minio_config()

  files_list = {}

  # Get the list of files to be uploaded. We only need the JSON files
  for f in os.listdir(cfg.output_path):
    if f.endswith(".json"):
      # Process only if no output parquet file exists for this JSON file
      base_f  = os.path.splitext(f)[0]
      check_f = "weather.header_{}.parquet".format(base_f[12:])
      full_f  = os.path.join(cfg.output_path, f)

      if not os.path.exists(os.path.join(cfg.output_path, check_f)):
        files_list[full_f] = base_f[12:]


  total_files = len(files_list)
  file_count = 0
  log.info("Count of JSON files to process: {}".format(total_files))

  if total_files:
    for f, suffix in files_list.items():
      f2 = open(f, 'r')
      data = json.loads(f2.read())
      f2.close()

      # Parse the weather data accordingly
      log.info("Processing JSON data file: {}".format(f))
      weather_header  = get_weather_header(data)
      weather_units   = get_weather_units(data)
      weather_current = get_weather_current(data)
      weather_hourly  = get_weather_hourly(data)

      # Save to parquet files
      log.info("Saving processed data to parquet files")
      weather_header.to_parquet(os.path.join(
                    cfg.output_path, "weather.header_{}.parquet".format(suffix)))

      weather_units.to_parquet(os.path.join(
                    cfg.output_path, "weather.units_{}.parquet".format(suffix)))

      weather_current.to_parquet(os.path.join(
                    cfg.output_path, "weather.current_{}.parquet".format(suffix)))

      weather_hourly.to_parquet(os.path.join(
                    cfg.output_path, "weather.hourly_{}.parquet".format(suffix)))

      file_count += 1


  log.info("Total weather data processed: {} out of {}".format(file_count, total_files))

  output = { 'total_files': total_files,
             'total_processed': file_count,
           }
  print(json.dumps(output))

