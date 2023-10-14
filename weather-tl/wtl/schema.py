from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime

class WmoCodeBase(BaseModel):
  code: int
  description: str

class WmoCode(WmoCodeBase):
  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)


class WeatherUnitBase(BaseModel):
  unit_type: str
  unit_code: str
  unit: str

class WeatherUnit(WeatherUnitBase):
  id: int
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)


