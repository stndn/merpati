# Merpati - Weather TL

Transform data stored in S3 bucket and load into database for reporting and API usage.

## Introduction

The weather-TL component of `Merpati` is a proof-of-concept application to complement [Garudata][url-garudata], the showcase for TL process of data platform. It is part of the bigger end-to-end data platform showcase.

This component contains simplified modules where stored data are transformed and stored as dataset for use by data consumers, both application and reporting tool.

The Weather-TL component consists of two major sub-components:
1. Modules to transform and load the data into denormalized datasets suitable for reporting purpose
1. Modules to transform and load the data into normalized datasets suitable for consumptions by API and applications

As of this writing, the focus will be on denormalized datasets, suitable for consumption by BI tools such as [Apache Superset][url-superset].

Further, while the plan is to use [Apache Spark][url-apache-spark], it is currently placed in backlog due to time constraint.


## Usage

### Dependencies

1. [Python][url-python] + [pyenv][url-pyenv] (Note: This project uses Python 3.10)
1. [Python venv][url-venv] - Python virtual environment
1. Additional Python libraries as defined in [`requirements.txt`][url-requirements]
1. Existing database schema with appropriate username, password, schema, and access set up


### Setup

Start by making a copy of [.env.sample file][url-dotenv-sample] and save as `.env`. Adjust the content as necessary, depending on whether the script will be running in development or production environment.

To fulfill the database target requirements, ensure that the target database with the right username/password is defined. Example:
```
CREATE USER db_warehouse_user with password 'sample-strong-password--j_d2agwGzHTrP4h3e--please replace'
CREATE DATABASE db_warehouse OWNER db_warehouse_user;
```


### Makefile

To simplify the setup and script execution, most of the commands are placed in [Makefile][url-makefile].

To download and install all the required libraries (as defined in [requirements.txt][url-requirements]):
```
make venv
```


### Database setup

For the database setup, we use [SQLAlchemy's Alembic][url-alembic] to manage the database migrations.

Initial alembic setup can be done by:
```
make alembic-init
```

The command above will setup alembic to make use of the configurations in this module.

To create the migration script (based on the [database model][url-db-model]), execute the following commands in the base directory of `weather-tl`:
```
./venv/bin/alembic revision --autogenerate -m "Initial DB setup"
./venv/bin/alembic upgrade head
```

The commands above will auto generate the database upgrade and downgrade script, followed with applying the database upgrade process.

Once that is done, make sure to feed the reference table by loading the [reference data][url-reference-data] into the newly-created database (adjust the username/hostname/dbname as appropriate):
```
psql -U db_warehouse_user -h 127.0.0.1 -f setup/01-reference-data.sql -d db_warehouse
```


### Usage


For the first component, used to transform and load the data into denormalized datasets, the commands are as follows:
```
# Extract JSON files to get and process current weather information and store in database
make current-weather-dataset

# Extract JSON files to get and process hourly weather forecasts and store in database
make hourly-weather-dataset

# The two commands above will create list of objects in S3 that have been processed
# The last command will move the objects to archive based on the list created above
make archive-weather-json
```


## Additional information

For faster insertion from Panda's DataFrame to PostgreSQL, refer to the methods mentioned in [this StackOverflow post][url-so-bulk-insert] and [this blog][url-pandas-df-to-psql]



<!-- Links -->
[url-garudata]: https://github.com/stndn/garudata
[url-superset]: https://github.com/stndn/garudata/tree/main/superset
[url-apache-spark]: https://spark.apache.org/ "Apache Spark"
[url-garudata-technology]: https://github.com/stndn/garudata#technology
[url-python]: https://www.python.org/
[url-pyenv]: https://github.com/pyenv/pyenv
[url-venv]: https://docs.python.org/3/library/venv.html
[url-requirements]: /weather-tl/requirements.txt
[url-dotenv-sample]: /weather-tl/.env.sample
[url-makefile]: /weather-tl/Makefile
[url-alembic]: https://alembic.sqlalchemy.org/en/latest/ "Alembic"
[url-db-model]: /weather-tl/wtl/models.py
[url-reference-data]: /weather-tl/setup/01-reference-data.sql "SQL script with commands to insert reference data"
[url-so-bulk-insert]: https://stackoverflow.com/a/44179612/1457788
[url-pandas-df-to-psql]: https://ellisvalentiner.com/post/a-fast-method-to-insert-a-pandas-dataframe-into-postgres/

