# system python interpreter. Used to create virtual environment
PY = python3
VENV = venv
BIN = $(VENV)/bin

# Read environment variable from file
include .env
VARS:=$(shell sed -ne 's/ *\#.*$$//; /./ s/=.*$$// p' .env )
$(foreach v,$(VARS),$(eval $(shell echo export $(v)='$($(v))')))


pip:
	$(BIN)/pip install --upgrade pip

$(VENV): requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install -r requirements.txt
	touch $(VENV)

.PHONY: test
test: $(VENV)
	$(BIN)/pytest

.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name __pycache__ -delete

.PHONY: cleanall
cleanall: clean
	rm -rf venv

.PHONY: load-env
load-env:
	source ./.env

alembic-init: $(VENV)
	VENV=$(VENV) sh ./setup/alembic-init.sh

current-weather-dataset: $(VENV)
	$(BIN)/$(PY) create_current_weather_dataset.py

hourly-weather-dataset: $(VENV)
	$(BIN)/$(PY) create_hourly_weather_dataset.py


# References:
# - https://earthly.dev/blog/python-makefile/
# - https://github.com/venthur/gscholar/blob/master/makefile
# - https://stackoverflow.com/questions/44628206/how-to-load-and-export-variables-from-an-env-file-in-makefile
# - https://stackoverflow.com/questions/58602758/basic-if-else-statement-in-makefile

