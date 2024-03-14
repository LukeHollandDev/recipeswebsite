import time, requests
from playwright.async_api import async_playwright
from models import (
    Recipe,
    Nutrient,
    Ingredient,
    IngredientGroup,
    Instruction,
    InstructionGroup,
    Resource,
)
from utils import convert_to_minutes


class HelloFresh:
    name = "Hello Fresh"
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
    # Other
    image_host = (
        "https://img.hellofresh.com/w_384,q_auto,f_auto,c_limit,fl_lossy/hellofresh_s3"
    )

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

    def transform_recipes(self, recipes):
        # Remove any recipe which is just an add on or has empty ingredients or yields
        recipes = [
            recipe
            for recipe in recipes
            if not recipe.get("isAddon", False)
            and recipe.get("ingredients", []) != []
            and recipe.get("yields", []) != []
        ]

        transformed = []
        for recipe in recipes:
            nutrition = [
                Nutrient(**nutrient) for nutrient in recipe.get("nutrition", [])
            ]

            # Build list of ingredient ids mapped to names
            ingredient_map = {}
            for ingredient in recipe.get("ingredients", []):
                ingredient_map[ingredient.get("id")] = ingredient.get("name")

            # Get the ingredient amounts from the yields = 2 in yields
            yields = recipe.get("yields", [])
            # Potentially invalid if it does not have any yields
            if len(yields) == 0:
                continue
            # If the yields dont have units then it is not useful
            if not (
                yields[0].get("ingredients", [])
                and len(yields[0].get("ingredients", [])) > 0
            ):
                continue

            # Build the ingredients list using the yields and ingredient map
            ingredients = [
                IngredientGroup(
                    name=None,
                    ingredients=[
                        Ingredient(
                            name=ingredient_map.get(ingred_yield.get("id")),
                            amount_lower=(
                                float(ingred_yield.get("amount"))
                                if ingred_yield.get("amount")
                                else None
                            ),
                            amount_upper=(
                                float(ingred_yield.get("amount"))
                                if ingred_yield.get("amount")
                                else None
                            ),
                            unit=ingred_yield.get("unit"),
                            note=None,
                        )
                        for ingred_yield in yields[0].get("ingredients", [])
                    ],
                )
            ]

            # Has no instructions / steps in the recipe, ignore the recipe
            if len(recipe.get("steps", [])) == 0:
                continue

            instructions = [
                InstructionGroup(
                    name=None,
                    instructions=[
                        Instruction(
                            index=index,
                            text=step.get("instructions"),
                            image=(
                                f"{self.image_host}{step.get('images', [])[0].get('path')}"
                                if len(step.get("images", [])) > 0
                                else None
                            ),
                        )
                        for index, step in enumerate(recipe.get("steps", []))
                    ],
                )
            ]

            additional_resources = []
            if recipe.get("cardLink"):
                additional_resources.append(
                    Resource(
                        name="Recipe Card PDF", type="PDF", value=recipe.get("cardLink")
                    )
                )

            cuisine = None
            if recipe.get("cuisines", []):
                cuisine = recipe.get("cuisines", [])[0].get("name")

            # Convert the prep and total into integer minutes
            recipe["prepTime"] = convert_to_minutes(recipe.get("prepTime"))
            # totalTime in hello fresh is actually cooking time, so combine prep and cook time
            recipe["totalTime"] = convert_to_minutes(recipe.get("totalTime"))
            if recipe["totalTime"]:
                recipe["totalTime"] = recipe["totalTime"] + recipe["prepTime"]

            transformed.append(
                Recipe(
                    id=recipe.get("id"),
                    title=recipe.get("name"),
                    description=recipe.get("description"),
                    url=recipe.get("websiteUrl"),
                    image=f"{self.image_host}{recipe.get('imagePath')}",
                    cuisine=cuisine,
                    prepTime=recipe.get("prepTime"),
                    totalTime=recipe.get("totalTime"),
                    servings=yields[0].get("yields"),
                    nutrition=nutrition,
                    ingredients=ingredients,
                    instructions=instructions,
                    additional_resources=additional_resources,
                )
            )

        return transformed

    # Helper methods:

    async def set_bearer_from_api_request(self, request):
        if request.url.startswith(self.recipe_api_url):
            headers = await request.all_headers()
            if "authorization" in headers:
                self.bearer_token = headers["authorization"].split(" ")[1]
