from typing import Any
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


class BaseModel(object):
  __abstract__ = True

  # Default __repr__ adopted from https://stackoverflow.com/a/54034962/
  def __repr__(self):
      fmt = u'{}.{}({})'
      package = self.__class__.__module__
      class_ = self.__class__.__name__
      attrs = [
          (k, getattr(self, k)) for k in self.__mapper__.columns.keys()
      ]
      sattrs = u', '.join('{}={!r}'.format(*x) for x in attrs)
      return fmt.format(package, class_, sattrs)


Base: Any = declarative_base(cls=BaseModel)


class WmoCode(Base):
  __tablename__ = 'wmo_codes'
  id            = sa.Column(sa.SmallInteger, sa.Identity(always=True), primary_key=True)
  code          = sa.Column(sa.SmallInteger, unique=True, nullable=False)
  description   = sa.Column(sa.String(40), nullable=False)
  created_at    = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
  updated_at    = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class WeatherUnit(Base):
  __tablename__ = 'weather_units'
  id            = sa.Column(sa.SmallInteger, sa.Identity(always=True), primary_key=True)
  unit_type     = sa.Column(sa.String(16), nullable=False)
  unit_code     = sa.Column(sa.String(4), nullable=False)
  unit          = sa.Column(sa.String(10), nullable=False)
  created_at    = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
  updated_at    = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class CurrentWeather(Base):
  __tablename__       = 'current_weathers'
  id                  = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
  uuid                = sa.Column(sa.String(32), nullable=False)
  location_name       = sa.Column(sa.String(64), nullable=False)
  location_country    = sa.Column(sa.String(64), nullable=False)
  location_latitude   = sa.Column(sa.Numeric(11, 8), nullable=False)
  location_longitude  = sa.Column(sa.Numeric(11, 8), nullable=False)
  data_latitude       = sa.Column(sa.Numeric(11, 8), nullable=False)
  data_longitude      = sa.Column(sa.Numeric(11, 8), nullable=False)
  distance            = sa.Column(sa.REAL, nullable=False)
  timezone            = sa.Column(sa.String(32), nullable=False)
  timezone_short      = sa.Column(sa.String(16), nullable=False)
  utc_offset_seconds  = sa.Column(sa.Integer, nullable=False)
  elevation           = sa.Column(sa.REAL, nullable=False)
  temperature_c       = sa.Column(sa.REAL, nullable=False)
  temperature_f       = sa.Column(sa.REAL, nullable=False)
  windspeed_kmh       = sa.Column(sa.REAL, nullable=False)
  windspeed_ms        = sa.Column(sa.REAL, nullable=False)
  windspeed_mph       = sa.Column(sa.REAL, nullable=False)
  windspeed_kn        = sa.Column(sa.REAL, nullable=False)
  winddirection       = sa.Column(sa.REAL, nullable=False)
  weathercode         = sa.Column(sa.SmallInteger, nullable=False)
  is_day              = sa.Column(sa.Boolean, nullable=False)
  data_timestamp      = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
  data_timestamp_utc  = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
  created_at          = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
  updated_at          = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class WeatherForecast(Base):
  __tablename__             = 'weather_forecasts'
  id                        = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
  uuid                      = sa.Column(sa.String(32), nullable=False)
  location_name             = sa.Column(sa.String(64), nullable=False)
  location_country          = sa.Column(sa.String(64), nullable=False)
  location_latitude         = sa.Column(sa.Numeric(11, 8), nullable=False)
  location_longitude        = sa.Column(sa.Numeric(11, 8), nullable=False)
  data_latitude             = sa.Column(sa.Numeric(11, 8), nullable=False)
  data_longitude            = sa.Column(sa.Numeric(11, 8), nullable=False)
  distance                  = sa.Column(sa.REAL, nullable=False)
  timezone                  = sa.Column(sa.String(32), nullable=False)
  timezone_short            = sa.Column(sa.String(16), nullable=False)
  utc_offset_seconds        = sa.Column(sa.Integer, nullable=False)
  elevation                 = sa.Column(sa.REAL, nullable=False)
  temperature_2m_c          = sa.Column(sa.REAL, nullable=False)
  temperature_2m_f          = sa.Column(sa.REAL, nullable=False)
  apparent_temperature_c    = sa.Column(sa.REAL, nullable=False)
  apparent_temperature_f    = sa.Column(sa.REAL, nullable=False)
  windspeed_10m_kmh         = sa.Column(sa.REAL, nullable=False)
  windspeed_10m_ms          = sa.Column(sa.REAL, nullable=False)
  windspeed_10m_mph         = sa.Column(sa.REAL, nullable=False)
  windspeed_10m_kn          = sa.Column(sa.REAL, nullable=False)
  winddirection_10          = sa.Column(sa.REAL, nullable=False)
  relativehumidity_2m       = sa.Column(sa.REAL, nullable=False)
  precipitation_probability = sa.Column(sa.REAL, nullable=False)
  precipitation_mm          = sa.Column(sa.REAL, nullable=False)
  precipitation_in          = sa.Column(sa.REAL, nullable=False)
  weathercode               = sa.Column(sa.SmallInteger, nullable=False)
  forecast_timestamp        = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
  forecast_timestamp_utc    = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
  is_day                    = sa.Column(sa.Boolean, nullable=False)
  data_timestamp            = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
  data_timestamp_utc        = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False)
  created_at                = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
  updated_at                = sa.Column(sa.TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

