import os
import errno
from geopy import distance


"""
Ensure path exists
Ref1: https://stackoverflow.com/questions/32123394/workflow-to-create-a-folder-if-it-doesnt-exist-already
Ref2: https://stackoverflow.com/questions/273192/how-do-i-create-a-directory-and-any-missing-parent-directories
"""
def make_sure_path_exists(path):
  try:
    os.makedirs(path)
  except OSError as exception:
    if exception.errno != errno.EEXIST:
      raise


def celcius_to_fahrenheit(temperature: float) -> float:
  return (temperature * 9 / 5) + 32


def kmh_to_ms(speed: float) -> float:
  return speed * 5 / 18


def kmh_to_mph(speed: float) -> float:
  return speed / 1.609344


def kmh_to_knot(speed: float) -> float:
  return speed / 1.852


def mm_to_inch(precipitation: float) -> float:
  return precipitation / 25.4


def calculate_distance(lat1: float, long1: float, lat2: float, long2: float) -> float:
  loc1 = (lat1, long1)
  loc2 = (lat2, long2)

  return [ distance.distance(loc1, loc2).km, distance.distance(loc1, loc2).mi ]
