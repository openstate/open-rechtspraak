.PHONY: build destroy down logs reset schema up test

COMPOSE = docker compose -f docker-compose.yml -f docker-compose-dev.yml
FLASK = $(COMPOSE) run --rm app flask
WEBPACK = $(COMPOSE) run --rm webpack

build: .env
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
	$(COMPOSE) exec app pytest ${TEST_PATH}

cli:
	$(COMPOSE) exec app bash

.env:
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
