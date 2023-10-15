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
Initialize MinIO configuration

Return
  Dictionary of MinIO configuration
"""
def init_minio_config() -> dict:
  return {  'url'           : os.getenv('MINIO_URL', None),
            'access_key'    : os.getenv('MINIO_ACCESS_KEY', None),
            'secret_key'    : os.getenv('MINIO_SECRET_KEY', None),
            'bucket_w_in'   : os.getenv('MINIO_BUCKET_W_IN', None),
            'bucket_w_out'  : os.getenv('MINIO_BUCKET_W_OUT', None),
         }

