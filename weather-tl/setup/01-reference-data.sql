INSERT INTO wmo_codes (code, description) VALUES
  (0,   'Clear sky'),
  (1,   'Mainly clear'),
  (2,   'Partly cloudy'),
  (3,   'Overcast'),
  (45,  'Fog'),
  (48,  'Depositing rime fog'),
  (51,  'Drizzle: Light intensity'),
  (53,  'Drizzle: Moderate intensity'),
  (55,  'Drizzle: Dense intensity'),
  (56,  'Freezing drizzle: Light intensity'),
  (57,  'Freezing drizzle: Dense intensity'),
  (61,  'Rain: Slight intensity'),
  (63,  'Rain: Moderate intensity'),
  (65,  'Rain: Heavy intensity'),
  (66,  'Freezing rain: Light intensity'),
  (67,  'Freezing rain: Heavy intensity'),
  (71,  'Snow fall: Slight intensity'),
  (73,  'Snow fall: Moderate intensity'),
  (75,  'Snow fall: Heavy intensity'),
  (77,  'Snow grains'),
  (80,  'Rain showers: Slight'),
  (81,  'Rain showers: Moderate'),
  (82,  'Rain showers: Violent'),
  (85,  'Snow showers: Slight'),
  (86,  'Snow showers: Heavy'),
  (95,  'Thunderstorm: Slight or moderate'),
  (96,  'Thunderstorm with slight hail'),
  (99,  'Thunderstorm with heavy hail')
  ;


INSERT INTO weather_units (unit_type, unit_code, unit) VALUES
  ('temperature',               'c',    '°C'),
  ('temperature',               'f',    '°F'),
  ('windspeed',                 'kmh',  'Km/h'),
  ('windspeed',                 'ms',   'm/s'),
  ('windspeed',                 'mph',  'Mph'),
  ('windspeed',                 'kn',   'Knots'),
  ('winddirection',             'deg',  '°'),
  ('relativehumidity',          'pct',  '%'),
  ('probability',               'pct',  '%'),
  ('precipitation',             'mm',   'Millimeter'),
  ('precipitation',             'in',   'Inch')
  ;

