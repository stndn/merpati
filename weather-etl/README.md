# Merpati - Weather ETL

Extract, Transform, and Load weather information as provided by [Open-Meteo API][url-open-meteo] into S3 storage.

## Introduction

The weather-ETL component of `Merpati` is a proof-of-concept application to complement [Garudata][url-garudata], the showcase the ETL process of data platform. It is part of the bigger end-to-end data platform showcase.

This component contains simplified modules where data may be downloaded, generated, processed, and stored as part of data source.


The weather component consists of three modules:
1. Get-weather: Integrates with Open-Meteo's API using Python's `requests` to download weather information for locations defined in [config/locations.json][url-config-locations].
1. Process-weather: Extract the weather data into headers, current weather, hourly weather, and the units information into separate Parquet files
1. Save-weather: Stores the retrieved weather information into object store

For the object store, we will use MinIO.


## How It Works

In processing end-to-end data, `Merpati` takes on two approaches at once:
1. Extract and Load (EL): Retrieve the weather data from [Open-Meteo][url-open-meteo], save as JSON, and store the data into S3 bucket. Additional processing metadata is inserted into the final JSON (e.g. Name of the target location and the geographical points), but no data transformation is involved
2. Extract, Transform, and Load (ETL): Using the raw JSON data file from the calls to [Open-Meteo][url-open-meteo], the data is [parsed][url-parse-weather] and transformed into four related Parquet files. Each of the files contains basic metadata such as timestamp and location information, such that they can be used to build up usable datasets without having to combine all the Parquet files together

Both EL and ETL approach provide raw datasets that can be used as input to the next [data transformation and load][url-weather-tl] step, to produce datasets that are ready for consumption by reporting tools and API's.


## Usage

### Dependencies

1. [Python][url-python] + [pyenv][url-pyenv] (Note: This project uses Python 3.10)
1. [Python venv][url-venv] - Python virtual environment
1. [requests][url-requests] - Python library
1. [pandas][url-pandas] - Python library
1. Weather API from [Open-Meteo][url-open-meteo]


### Setup

Start by making a copy of [.env.sample file][url-dotenv-sample] and save as `.env`. Adjust the content as necessary, depending on whether the script will be running in development or production environment.


To simplify the setup and script execution, most of the commands are placed in [Makefile][url-makefile].

To download and install all the required libraries (as defined in [requirements.txt][url-requirements]):
```
make venv
```

To download the weather information from Open-Meteo:
```
make get-weather
```

This will connect to the Open-Meteo API and download the weather information as defined in the script. The output will be saved in the `output` directory.


To further process the weather data into multiple Parquet files, execute:
```
make process-weather
```

Finally, save the files into S3:
```
make save-weather
```


## Additional information

[Open-Meteo][url-open-meteo] is an open-source weather API and offers free access for non-commercial use.


<!-- Links -->
[url-open-meteo]: https://open-meteo.com/ "Open-Meteo: The open-source weather API"
[url-garudata]: https://github.com/stndn/garudata "Garudata - The data platform project"
[url-config-locations]: /weather-etl/config/locations.json "Locations to download the weather information of"
[url-python]: https://www.python.org/
[url-pyenv]: https://github.com/pyenv/pyenv
[url-venv]: https://docs.python.org/3/library/venv.html
[url-requests]: https://pypi.org/project/requests/
[url-pandas]: https://pandas.pydata.org/
[url-dotenv-sample]: /weather-etl/.env.sample
[url-makefile]: /weather-etl/Makefile
[url-requirements]: /weather-etl/requirements.txt
[url-parse-weather]: /weather-etl/parse_weather.py
[url-weather-tl]: /weather-tl
