# HelloFreshed 2 - Frontend

This directory contains the code for the frontend of HelloFreshed 2.

## Running Locally

To run this code locally you;

* Make sure NodeJS and NPM is installed
* Install dependencies `npm install`
* Run the local server `npm run dev`

To test the build artifact;

* Build the website `npm run build`
* Serve/preview the website `npm run preview`

To lint and test the project;

* Lint `npm run lint`
* Test `npm run test`

*Tests need to be added/implemented.*

## Project Layout (src directory)

* assets/ - shared assets like images
* components/ - re-usable components of the site
* routes/ - pages
* routeTree.gen.ts - auto generated route configuration
* vite-env.d.ts - vite typescript typing
* app.tsx - application entry point