# Merpati

The data messenger, designed to run on top of the [Garudata data platform][url-garudata].

The application consists of multiple components that make use of different tools available in the data platform.

## Application Components

[Weather-ETL][url-weather-etl]: Component to retrieve weather information from Open Meteo API, which is minimally transformed and saved as local files before being stored into S3 object storage.
[Weather-TL][url-weather-tl]: Component to transform the weather data files stored in S3 object storagea and store the data into PostgreSQL data warehouse.


<!-- Links -->
[url-garudata]: https://github.com/stndn/garudata "Garudata - The data platform project"
[url-weather-etl]: /weather-etl "The weather data retriever, transformer, and loader"
[url-weather-tl]: /weather-tl "The weather data retriever"

