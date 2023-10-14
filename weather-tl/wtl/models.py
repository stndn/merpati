from typing import Any
from datetime import datetime

import sqlalchemy as sa
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
  id            = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
  code          = sa.Column(sa.SmallInteger, nullable=False)
  description   = sa.Column(sa.String(40), nullable=False)
  created_at    = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
  updated_at    = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)


class WeatherUnit(Base):
  __tablename__ = 'weather_units'
  id            = sa.Column(sa.Integer, sa.Identity(always=True), primary_key=True)
  unit_type     = sa.Column(sa.String(16), nullable=False)
  unit_code     = sa.Column(sa.String(4), nullable=False)
  unit          = sa.Column(sa.String(10), nullable=False)
  created_at    = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
  updated_at    = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)

