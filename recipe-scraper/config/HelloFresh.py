import time, json, requests
from playwright.async_api import async_playwright


class HelloFresh:
    # Bearer attributes
    bearer_required = True
    bearer_url = "https://www.hellofresh.co.uk/recipes/search?q=chicken"
    bearer_token = None
    # Recipe API attributes
    recipe_api_url = "https://www.hellofresh.co.uk/gw/recipes/recipes/search"
    recipe_params = {
        "country": "GB",
        "locale": "en-GB",
        "take": 250,
        "skip": 0,
        "sort": "date",  # -date for ascending
    }
    recipe_headers = {}

    async def set_bearer_from_api_request(self, request):
        if request.url.startswith(self.recipe_api_url):
            headers = await request.all_headers()
            if "authorization" in headers:
                self.bearer_token = headers["authorization"].split(" ")[1]

    async def set_bearer_token(self):
        # Using playwright to visit the website and watch the network requests to get the bearer token
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            # Event handler for requests, bearer token is set in the set_bearer_from_api_request method
            page.on("request", self.set_bearer_from_api_request)
            await page.goto(self.bearer_url)
            time.sleep(2)
            await browser.close()

    def get_recipes(self):
        if not self.bearer_token:
            print("Bearer token not set")
            return

        # Make a request to the recipe API using the bearer token
        self.recipe_headers["Authorization"] = f"Bearer {self.bearer_token}"
        response = requests.get(
            self.recipe_api_url,
            params=self.recipe_params,
            headers=self.recipe_headers,
        )

        recipes = []
        if response.status_code == 200:
            total = response.json().get("total", 0)
            print(f"Total recipes to obtain: {total}")
            while total > self.recipe_params["skip"]:
                # Add the recipes to the list
                recipes.extend(response.json().get("items", []))
                # If we have obtained all the recipes, break out of the loop
                if len(recipes) >= total:
                    print("All recipes obtained")
                    break
                # Update the skip parameter to get the next set of recipes
                self.recipe_params["skip"] += self.recipe_params["take"]
                response = requests.get(
                    self.recipe_api_url,
                    params=self.recipe_params,
                    headers=self.recipe_headers,
                )
                # If the request fails, try again with a different sort order
                if response.status_code != 200:
                    if (
                        self.recipe_params["skip"] >= 10000
                        and self.recipe_params["sort"] == "date"
                    ):
                        print("Reached 10,000 elastic limit, now using -date sort")
                        self.recipe_params["sort"] = "-date"
                        self.recipe_params["skip"] = 0
                    else:
                        print(f"Failed to get recipes: {response.text}")
                        print(f"Params at time of failure: {self.recipe_params}")
                        break
                # Sleep to avoid rate limiting
                time.sleep(0.1)
            return recipes
        else:
            print(f"Failed to get recipes: {response.text}")
