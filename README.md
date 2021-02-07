# Open Rechtspraak

## Requirements
- docker-compose
- Make (to access dev shortcuts in [Makefile](/Makefile))

## Stack
- Python 3.8.6+
- Flask
- Postgres 13

## Getting started
- You can initialize the full development environment with `make init`.
- Pre-commit hooks are configured, and it is recommended you install them through `pre-commit install`.
- Seed is available with `make seed`.
- Visit [localhost:5000](localhost:5000).

### Did you make any changes to the code base?
- Run `make test` to run the test suite.
- Ensure you add tests for new functionalities.

## Periodically scraping data
Scraping data from people is done in two steps:
1. Retrieving a list of people with `make import_people` from the `https://namenlijst.rechtspraak.nl/Services/WebNamenlijstService/Zoek` service. These people are saved.
2. We enrich the details from people through `https://namenlijst.rechtspraak.nl/Services/WebNamenlijstService/haalOp/?id=<rechtspraak_id>` where `rechtspraak_id` is a unique ID assigned by `namenlijst.rechtspraak.nl` to the person.

## Protecting a scraped person from public eyes
The `People` model has an attribute called `protected`. Toggling that attribute to `True` removes the person from all public listings (i.e. the API search endpoint) and blocks access to their detail page.

## Contact details
Questions? Contact [developers@openstate.eu](mailto:developers@openstate.eu).
