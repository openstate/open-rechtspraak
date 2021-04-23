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

seed:
	$(FLASK) seed
