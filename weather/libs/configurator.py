import os
import json
import libs.helper as Helper
import logging, logging.config
from config.app_config import Config, Development, Production, Testing


"""
Initialize configuration based on environment key

Return:
  configuration
"""
def init_config() -> Config:
  ENV_KEY = 'APP_ENV'
  ENV_LIST = {'dev'   : Development,
              'prod'  : Production,
              'test'  : Testing,
             }

  ENV = os.getenv(ENV_KEY, None)

  if ENV is None:
    raise NameError(f"The environment variable '{ENV_KEY}' needs to be set")
  else:
    if ENV not in ENV_LIST:
      raise KeyError(ENV, ENV_LIST)
    else:
      return ENV_LIST[ENV]


"""
Initialize logger

Return
  logger
"""
def init_logger(name:str, log_path:str=None) -> logging:
  if log_path is None:
    log_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs'))

  Helper.make_sure_path_exists(log_path)

  logging.config.fileConfig('config/logging.ini',
                            defaults={'logpath': log_path}
                           )

  log = logging.getLogger(name)
  return log


"""
Load locations to work with

Return
  locations
"""
def load_locations(location_file:str) -> list:
  if not os.path.isfile(location_file):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), location_file)
  with open(location_file, 'r') as f:
    locations = json.load(f)
    return locations


