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


get-weather: $(VENV)
	$(BIN)/$(PY) get_weather.py

save-weather: $(VENV)
	$(BIN)/$(PY) save_weather.py


# References:
# - https://earthly.dev/blog/python-makefile/
# - https://github.com/venthur/gscholar/blob/master/makefile
# - https://stackoverflow.com/questions/44628206/how-to-load-and-export-variables-from-an-env-file-in-makefile

