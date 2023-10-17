# Application configuration

import os
from time import localtime, strftime

class Config(object):
  DEBUG = False
  TESTING = False
  app_version = "v1"
  APP_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
  tmp_path   = os.path.abspath(os.path.join(APP_PATH, 'tmp/'))

class Development(Config):
  DEBUG = True

class Production(Config):
  DEBUG = False

class Testing(Config):
  DEBUG = False
  TESTING=True

