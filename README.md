# HelloFreshed 2

Second iteration of HelloFreshed platform. Redesigned to be a better and useful platform.

OG HelloFreshed:

* https://hf.lukeh.xyz
* https://github.com/AmazonPriime/HelloFreshed

### Technologies

* FastAPI for the backend
  * Python
  * PostgreSQL
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