# Open Rechtspraak

## Requirements
- docker-compose
- Make (to access dev shortcuts in [Makefile](/Makefile))

## Stack

### Back end
- Python 3.8.6+
- Flask
- Postgres 13

### Front end
- Bootstrap 5 (v5.0.0-beta1)
- For JS see [package.json](/package.json)
- Webpacker for compilation

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

## Config for production
These env variables are required for production:
- `ENV` = `production`
- `FLASK_ENV` = `production`
- `DATABASE_URL` = url to the database, formatted similar to `postgresql://user:password@localhost:port/database_name` (alternatively you can use the individual parts of the database url in separate environment variables as found in [.env.dist](/.env.dist))
- `SECRET_KEY` = a randomly generated string that is used for encryption
- `LOG_LEVEL` = a valid level from Python's [logging](https://docs.python.org/3/library/logging.html) module; generally `WARN` or higher is recommended in production

## Prod deploys should contain at least...
- Compiling new assets, i.e. by running `npm run prod`
- Running the latest migrations, i.e. by running [release/tasks.sh](/release/tasks.sh)

## Contact details
Questions? Contact [developers@openstate.eu](mailto:developers@openstate.eu).
