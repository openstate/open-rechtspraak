# Open Rechtspraak

## Requirements
- docker-compose
- Make (to access dev shortcuts in [Makefile](/Makefile))

## Stack

### Back end
- Python 3.9+
- Flask
- Postgres 13

### Front end
- Bootstrap 5
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

Similarly, two commands exist for scraping verdicts and enriching them.
1. Retrieving a list of verdicts (default = verdicts of the past three days) with `make import_verdicts`.
2. Enriching verdicts with `make enrich_verdicts` in two steps: (1) collecting additional metadata of the verdict and (2) checking whether a person is mentioned in a verdict.

_Warning_: The number of verdicts imported by `make import_verdicts` can be high (ca. 50k a year). Consider this carefully when you use the `--start_date` and `--end_date` cli params.

## Protecting a scraped person from public eyes
The `People` model has an attribute called `protected`. Toggling that attribute to `True` removes the person from all public listings (i.e. the API search endpoint) and blocks access to their detail page.

## Config for production
These env variables are required for production:
- `ENV` = `production`
- `FLASK_ENV` = `production`
- `DATABASE_URL` = url to the database, formatted similar to `postgresql://user:password@localhost:port/database_name` (alternatively you can use the individual parts of the database url in separate environment variables as found in [.env.dist](/.env.dist))
- `SECRET_KEY` = a randomly generated string that is used for encryption
- `LOG_LEVEL` = a valid level from Python's [logging](https://docs.python.org/3/library/logging.html) module; generally `WARN` or higher is recommended in production

## How to deploy this app to production
1. Compiling new assets, i.e. by running `npm run prod`
2. Running the latest migrations, i.e. by running [release/tasks.sh](/release/tasks.sh)
3. Ensure a cron is running with the jobs mentioned in cron.sh

## Sitemap
- A self-updating sitemap is included at `/sitemap.xml`. You can submit this sitemap to search engines to be indexed faster.

## Contact details
Questions? Contact [developers@openstate.eu](mailto:developers@openstate.eu).

## Local dev
Without Flask in Docker, but a Docker based DB:
- `cp .env.dist .env`
- `export $(cat .env | xargs)`
- `export DATABASE_URL=postgresql://ors2user:ors2@localhost:54322/ors2`
