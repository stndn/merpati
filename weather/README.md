# Merpati - Weather

Retrieve and save weather information as provided by [Open Meteo API][url-open-meteo].

## Introduction

The weather component of `Merpati` is a proof-of-concept application to complement [Garudata][url-garudata], the showcase of end-to-end data platform.

It is built upon simple components where data may be downloaded, generated, and stored as part of data source.


The weather component consists of two modules:
1. Get-weather: Integrates with Open-Meteo's API using Python's `requests` to download weather information for locations defined in [config/locations.py][url-config-locations].
2. Save-weather: Stores the retrieved weather information into object store

For the object store, we will use MinIO.


## Usage

### Dependencies

1. [Python][url-python] + [pyenv][url-pyenv] (Note: This project uses Python 3.10)
2. [requests][url-requests] Python library
3. [pandas][url-pandas] Python library
4. Weather API from [Open-Meteo][url-open-meteo]


### Setup

Start by making a copy of [.env.sample file][url-dotenv-sample] and save as `.env`. Adjust the content as necessary, depending on whether the script will be running in development or production environment.


To simplify the setup and script execution, most of the commands are placed in [Makefile][url-makefile].

To download and install all the required libraries (as defined in [requirements.txt][url-requirements]):
```
make venv
```

To download the weather information from Open Meteo:
```
make get-weather
```

This will connect to the Open Meteo API and download the weather information as defined in the script. The output will be saved in the `output` directory.



### Workflow

1. API calls will be initiated via `get-weather` to get the latest weather data, which is saved as Parquet files in local (host) filesystem
1. A separate module `save-weather` will save the Parquet files into S3 bucket hosted in MinIO server


## Additional information

Open-Meteo is an open-source weather API and offers free access for non-commercial use.


<!-- Links -->
[url-open-meteo]: https://open-meteo.com/ "Open Meteo: The open-source weather API"
[url-garudata]: https://github.com/stndn/garudata "Garudata - The data platform project"
[url-config-locations]: /weather/config/locations.py "Locations to download the weather information of"
[url-python]: https://www.python.org/
[url-pyenv]: https://github.com/pyenv/pyenv
[url-requests]: https://pypi.org/project/requests/
[url-pandas]: https://pandas.pydata.org/
[url-dotenv-sample]: /weather/.env.sample
[url-makefile]: /weather/Makefile
[url-requirements]: /weather/requirements.txt
