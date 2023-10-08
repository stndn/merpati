import os
import json
import requests
import uuid
from libs import configurator
from libs import helper


if __name__ == '__main__':

  # Initialize all configurations
  cfg = configurator.init_config()
  log = configurator.init_logger(name='get_weather',
                               log_path=os.path.join(cfg.APP_PATH, 'logs')
                              )

  # Load locations to work with
  locations = configurator.load_locations(cfg.locations_file)

  helper.make_sure_path_exists(cfg.output_path)

  file_count = 0

  for loc in locations:
    log.info("Getting weather information for {} in {}, located at {}, {}" \
        .format(loc['name'], loc['country'], loc['latitude'], loc['longitude'])
            )

    url = cfg.open_meteo_weather_url.format(lat=loc['latitude'], long=loc['longitude'])

    weather_data = requests.get(url)
    weather_json = weather_data.json()

    # Add the location name and country for reference
    # Also, save the original requested coordinate since the output from Open-Meteo is a few km's away
    weather_json['uuid'] = uuid.uuid4().hex
    weather_json['location_name'] = loc['name']
    weather_json['location_country'] = loc['country']
    weather_json['location_latitude'] = loc['latitude']
    weather_json['location_longitude'] = loc['longitude']

    # Save the JSON file for later usage
    json_filename = "weather.all_{}_{}_{}.json".format(
                        loc['latitude'], loc['longitude'], cfg.outfile_suffix
                      )

    target_filename = os.path.join(cfg.output_path, json_filename)
    log.info("Saving weather data into {}".format(target_filename))
    with open(target_filename, 'w', encoding='utf-8') as f:
      json.dump(weather_json, f, ensure_ascii=False)
      file_count += 1


  log.info("Total weather data saved: {}".format(file_count))

  output = { 'total_processed': file_count }
  print(json.dumps(output))
