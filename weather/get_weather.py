import os
import json
import requests
import pandas as pd
from lib import configurator
from lib import helper


if __name__ == '__main__':

  # Initialize all configurations
  cfg = configurator.init_config()
  log = configurator.init_logger(name='log_app',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )

  # Load locations to work with
  locations = configurator.load_locations(cfg.locations_file)

  helper.make_sure_path_exists(cfg.output_path)


  for loc in locations:
    log.info("Getting weather information for {} in {}, located at {}, {}" \
        .format(loc['name'], loc['country'], loc['latitude'], loc['longitude'])
            )

    url = cfg.open_meteo_weather_url.format(lat=loc['latitude'], long=loc['longitude'])

    weather_data = requests.get(url)
    weather_json = weather_data.json()

    # Add the location name and country for reference
    weather_json['location_name'] = loc['name']
    weather_json['location_country'] = loc['country']

    # Read the data into Panda's data frame
    part1 = { d: weather_json[d] for d in weather_json if d not in { 'hourly' }}

    # Normalize the main data as header file, and save the hourly weather data separately
    df1 = pd.json_normalize(part1)
    df2 = pd.DataFrame(weather_json['hourly'])

    df1_filename = "{}_{}_{}_part1.parquet".format(cfg.outfile_prefix, loc['latitude'], loc['longitude'])
    df2_filename = "{}_{}_{}_part2.parquet".format(cfg.outfile_prefix, loc['latitude'], loc['longitude'])

    df1.to_parquet(os.path.join(cfg.output_path, df1_filename))
    df2.to_parquet(os.path.join(cfg.output_path, df2_filename))

