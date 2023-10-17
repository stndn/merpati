import csv
import json
import os

import pandas as pd

from io import StringIO
from libs import configurator
from libs import helper
from minio import Minio
from wtl import database


if __name__ == '__main__':

  # Initialize all configurations
  cfg = configurator.init_config()
  log = configurator.init_logger(name='create_hourly_weather_dataset',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )
  minio_cfg = configurator.init_minio_config()

  # Get the list of JSON files from MinIO bucket
  client = Minio(minio_cfg['url'], minio_cfg['access_key'], minio_cfg['secret_key'])

  total_object = 0

  if client:
    log.info("Connected to S3 bucket at {}".format(minio_cfg['url']))

    objects = client.list_objects(minio_cfg['bucket_w_in'], prefix='json/weather.all')

    obj_list = []
    total_processed = 0

    for obj in objects:
      log.info("Processing object: {}".format(obj.object_name))
      obj_list.append(obj.object_name)
      response = client.get_object(minio_cfg['bucket_w_in'], obj.object_name)

      content = json.loads(response.data.decode('utf8'))

      df = pd.DataFrame(content['hourly'])
      df.rename({ 'time'                : 'forecast_timestamp',
                  'temperature_2m'      : 'temperature_2m_c',
                  'apparent_temperature': 'apparent_temperature_c',
                  'windspeed_10m'       : 'windspeed_10m_kmh',
                  'precipitation'       : 'precipitation_mm',
                }, axis=1, inplace=True)


      data = { 'data_timestamp': content['current']['time'] }
      for col in ['uuid', 'location_name', 'location_country', 'location_latitude',
                  'location_longitude', 'latitude', 'longitude', 'utc_offset_seconds',
                  'timezone', 'timezone_abbreviation', 'elevation' ]:
        data[col] = content[col]

      df2 = pd.DataFrame.from_dict([data])

      # Combine the two dataframes
      df  = df.join(df2).ffill()
      df['utc_offset_seconds'] = df['utc_offset_seconds'].astype('int64')

      # Convert the data accordingly
      df['temperature_2m_f']        = helper.celcius_to_fahrenheit(df['temperature_2m_c'])
      df['apparent_temperature_f']  = helper.celcius_to_fahrenheit(df['apparent_temperature_c'])
      df['windspeed_10m_ms']        = helper.kmh_to_ms(df['windspeed_10m_kmh'])
      df['windspeed_10m_mph']       = helper.kmh_to_mph(df['windspeed_10m_kmh'])
      df['windspeed_10m_kn']        = helper.kmh_to_knot(df['windspeed_10m_kmh'])
      df['precipitation_in']        = helper.mm_to_inch(df['precipitation_mm'])

      df['distance_km'], df['distance_mi'] = helper.calculate_distance(
                                          data['location_latitude'], data['location_longitude'],
                                          data['latitude'], data['longitude']
                                        )

      ### Convert time to utc
      df['forecast_timestamp'] = pd.to_datetime(df['forecast_timestamp'])
      df['forecast_timestamp'] = (df.apply(lambda x: x['forecast_timestamp'].tz_localize(tz=data['timezone']), axis=1))
      df['forecast_timestamp_utc'] = (df.apply(lambda x: x['forecast_timestamp'].tz_convert('UTC'), axis=1))

      df['data_timestamp'] = pd.to_datetime(df['data_timestamp'])
      df['data_timestamp'] = (df.apply(lambda x: x['data_timestamp'].tz_localize(tz=data['timezone']), axis=1))
      df['data_timestamp_utc'] = (df.apply(lambda x: x['data_timestamp'].tz_convert('UTC'), axis=1))

      # Rename and reorder the data columns
      df.rename({ 'latitude'              : 'data_latitude',
                  'longitude'             : 'data_longitude',
                  'timezone_abbreviation' : 'timezone_short',
                }, axis=1, inplace=True)

      cols = ['uuid', 'location_name', 'location_country', 'location_latitude',
              'location_longitude', 'data_latitude', 'data_longitude', 'distance_km',
              'distance_mi', 'timezone', 'timezone_short', 'utc_offset_seconds',
              'elevation', 'temperature_2m_c', 'temperature_2m_f', 'apparent_temperature_c',
              'apparent_temperature_f', 'windspeed_10m_kmh', 'windspeed_10m_ms',
              'windspeed_10m_mph', 'windspeed_10m_kn', 'winddirection_10m',
              'relativehumidity_2m', 'precipitation_probability', 'precipitation_mm',
              'precipitation_in', 'weathercode', 'forecast_timestamp',
              'forecast_timestamp_utc', 'is_day', 'data_timestamp', 'data_timestamp_utc',
             ]
      df = df.reindex(columns=cols)

      sio = StringIO()
      writer = csv.writer(sio)
      writer.writerows(df.values)
      sio.seek(0)

      db = database.create_session()
      cursor = database.create_cursor(db)

      with cursor as c:
        c.copy_from(file=sio, table='weather_forecasts', columns=cols, sep=',')
        db.commit()

      total_processed += 1

    total_object = len(obj_list)
    output = { 'total_object': total_object,
               'total_processed': total_processed,
               'source_bucket': minio_cfg['bucket_w_in'] }

    # Save the list of processed objects to be moved to archive later
    if total_object:
      helper.make_sure_path_exists(cfg.tmp_path)
      target_filename = os.path.join(cfg.tmp_path, 'weather-json-objects.txt')
      log.info("Saving list of processed files into {}".format(target_filename))

      with open(target_filename, 'a', encoding='utf-8') as f:
        f.write("\n".join(obj_list))
        f.write("\n")

  else:
    log.error("Cannot connect to S3 bucket. Exiting.")
    output = { 'total_object': total_object,
               'total_processed': 0,
               'source_bucket': minio_cfg['bucket_w_in'] }

  print(json.dumps(output))
