# HelloFreshed 2

Second iteration of HelloFreshed platform. Redesigned to be a better and useful platform.

OG HelloFreshed:

* https://hf.lukeh.xyz
* https://github.com/AmazonPriime/HelloFreshed

### Technologies

* FastAPI for the backend
  * Python
  * PostgreSQL
    * SQLModel
    * Alembic 
* React for the frontend
  * Typescript
  * MUI (Material UI)
  * Static SPA
* Python for the recipe scraping
  * Request
  * Beautiful Soup 4

### Features

* View recipe ingredients
* Favourite recipes
* Build a menu for a week to plan out meals
* Build a shopping list based on a recipe or weekly menu
* Conversion between different units of measurements

Other more technical features:

* User authentication
  * Password authentication
  * Potentially add OAuth options

### Data Sourcing

* Hello Fresh API
  * Standardise the data retrieved from the Hello Fresh API.
* Other recipe providers
  * Need to look out and view how to retrieve these and make them work with other recipes
* User submitted recipes
  * Eventually allow users to submit recipes

### Running Developer Environment

There is a docker-compose file which can be used to quickly spin up an environment for the website.

There are a few environment variables required, there is a sample .env.sample file which contains the required ones.

These values should be replaced with their actual values, inside of a `.env` file.

* DATABASE_URL (set inside of the compose itself)
* BACKEND_SECRET_KEY (required in .env)

You can run it by using this command from the root directory: `docker-compose -f .\docker-compose-dev.yml --env-file ./config/.env.dev up -d`.

*Required docker to be installed on your system and a `.env` file called `.env.dev` inside of a `config` directory**