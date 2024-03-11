# HelloFreshed 2 - Backend

This directory contains the code for the backend of HelloFreshed 2.

### Running Locally

To run this code locally you can either;

* Run the `docker-compose-dev.yml` which will spin up a Postgres database and Python container
  * From root directory run `docker-compose -f .\docker-compose-dev.yml up -d`
    * Requires docker enginer, which can be installed from https://docs.docker.com/engine/install/ (Docker desktop is recommended)
* Install the Python dependencies and run the API directly in your terminal
  * Create virtual environment `python -m venv env`
  * Activate the environment `source ./env/bin/activate` (`./env/Scripts/activate` on Windows)
  * Install dependencies `pip install -r requirements.txt`
  * You will need to setup a Postgres database and ensure you have `DATABASE_URL` environment variable setup with the URL to the database

### Population Script

With a database running and the environment variable set, the population script can be run to add recipes to the database.

This can also be run from the python docker container if you're using the docker compose.

Run `python populate.py` from the `backend` directory while in the virtual environment setup earlier.

Since this uses the `recipe.json` files from the `recipes` directory they must exist and have content.

### Alembic Migrations

Database migrations are managed by Alembic.

* Upgrading database to latest migration run `alembic upgrade head` while in the virutal environment setup earlier.
* Creating a new migration (usually after updating the SQLModels in `backend/models` directory)
  * Run `alembic revision --autogenerate -m "<migration information>"`  while in the virutal environment setup earlier.