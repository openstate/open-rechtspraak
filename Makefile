.PHONY: test

COMPOSE = docker-compose
FLASK = $(COMPOSE) run --rm app flask

build: env
	$(COMPOSE) pull
	$(COMPOSE) build

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
	$(COMPOSE) exec -e FLASK_DEBUG=0 -e FLASK_ENV=test app pytest -rP

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
