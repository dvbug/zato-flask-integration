
.PHONY: test

ENV_NAME=zato-flask-env
APP_NAME=sampleapp
BIN_DIR=$(CURDIR)/$(ENV_NAME)/bin

default: run

install:
	virtualenv $(CURDIR)/$(ENV_NAME)
	$(BIN_DIR)/pip install -r $(CURDIR)/requirements.txt
	$(BIN_DIR)/python $(CURDIR)/$(APP_NAME)/setup.py develop
	$(BIN_DIR)/pip install -e $(CURDIR)/$(APP_NAME)

run:
	$(MAKE) install
	$(ENV_NAME)/bin/python $(APP_NAME)/customer.py

clean:
	rm -rf $(CURDIR)/$(ENV_NAME)
	rm -rf $(CURDIR)/build
	rm -rf $(CURDIR)/dist
	rm -rf $(CURDIR)/src/zato_flask_env.egg-info
	find $(CURDIR) -name '*.pyc' -exec rm {} \;
