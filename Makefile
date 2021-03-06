.PHONY: test

COMPOSE = docker-compose
FLASK = $(COMPOSE) run --rm app flask
WEBPACK = $(COMPOSE) run --rm webpack

build: env
	$(COMPOSE) pull
	$(COMPOSE) build
	$(WEBPACK) npm install

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

init: build up db-schema seed

logs:
	$(COMPOSE) logs --tail=500 -f

db-migration:
	$(FLASK) db migrate -m '$(MESSAGE)'

db-schema:
	$(FLASK) db upgrade

db-truncate:
	$(FLASK) db_truncate

test:
	$(COMPOSE) exec -e FLASK_DEBUG=0 -e FLASK_ENV=test app pytest

cli:
	$(COMPOSE) run --rm app bash

env:
	cp .env.dist .env

import_people:
	$(FLASK) import_people

enrich_people:
	$(FLASK) enrich_people

import_verdicts:
	$(FLASK) import_verdicts

enrich_verdicts:
	$(FLASK) enrich_verdicts

import_static: import_institutions import_procedure_types import_legal_areas

import_institutions:
	$(FLASK) import_institutions

import_legal_areas:
	$(FLASK) import_legal_areas

import_procedure_types:
	$(FLASK) import_procedure_types

seed:
	$(FLASK) seed
