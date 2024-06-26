import requests, re, time
from bs4 import BeautifulSoup
from models import (
    Recipe,
    Nutrient,
    Ingredient,
    IngredientGroup,
    Instruction,
    InstructionGroup,
)
from utils import covert_float, convert_to_minutes


class JustOneCookbook:
    name = "Just One Cookbook"
    # Bearer attributes
    bearer_required = False
    # URLs
    recipe_url = "https://www.justonecookbook.com/wprm_print/"
    recipe_page_list_url = "https://www.justonecookbook.com/recipes/page/"

    def get_recipes(self):
        recipe_ids = self.get_recipe_ids()

        # Scrape the recipes using the recipe ids
        recipes = []
        for recipe_id in recipe_ids:
            response = requests.get(f"{self.recipe_url}{recipe_id}")
            response_content = response.content

            soup = BeautifulSoup(response_content, "html.parser")

            # Get the details of the recipe
            recipe = {
                "id": recipe_id,
                "title": soup.find("h2", class_="wprm-recipe-name").text,
                "description": soup.find("div", class_="wprm-recipe-summary").text,
                "url": soup.find("a", class_="wprm-print-button")["href"],
                "image": (
                    soup.find("div", class_="wprm-recipe-image").find("img")["src"]
                    if soup.find("div", class_="wprm-recipe-image").find("img")
                    else None
                ),
                "cuisine": (
                    soup.find("span", class_="wprm-recipe-cuisine").text
                    if soup.find("span", class_="wprm-recipe-cuisine")
                    else None
                ),
                "prepTime": (
                    soup.find("span", class_="wprm-recipe-prep_time").text
                    if soup.find("span", class_="wprm-recipe-prep_time")
                    else None
                ),
                "totalTime": (
                    soup.find("span", class_="wprm-recipe-total_time").text
                    if soup.find("span", class_="wprm-recipe-total_time")
                    else None
                ),
                "servings": (
                    soup.find("span", class_="wprm-recipe-servings").text
                    if soup.find("span", class_="wprm-recipe-servings")
                    else None
                ),
                "nutrition": [
                    self.extract_nutrition(nutrition)
                    for nutrition in soup.find_all(
                        "span", class_="wprm-nutrition-label-text-nutrition-container"
                    )
                ],
                "ingredients": [
                    self.extract_ingredient(ingredient_group)
                    for ingredient_group in soup.find_all(
                        "div", class_="wprm-recipe-ingredient-group"
                    )
                ],
                "instructions": [
                    self.extract_instruction(instruction_group)
                    for instruction_group in soup.find_all(
                        "div", class_="wprm-recipe-instruction-group"
                    )
                ],
            }
            recipes.append(recipe)
        return recipes

    @staticmethod
    def transform_recipes(recipes):
        transformed = []
        for recipe in recipes:
            nutrition = [
                Nutrient(
                    name=nutrient.get("name").replace(": ", ""),
                    amount=covert_float(nutrient.get("amount"))[0],
                    unit=nutrient.get("unit"),
                )
                for nutrient in recipe.get("nutrition", [])
            ]
            ingredients = [
                IngredientGroup(
                    name=ingredient.get("group_name"),
                    ingredients=[
                        Ingredient(
                            name=ingred.get("name"),
                            amount_lower=covert_float(ingred.get("amount"))[0],
                            amount_upper=covert_float(ingred.get("amount"))[1],
                            unit=ingred.get("unit"),
                            note=ingred.get("note"),
                        )
                        for ingred in ingredient.get("ingredients", [])
                    ],
                )
                for ingredient in recipe["ingredients"]
            ]
            instructions = [
                InstructionGroup(
                    name=instruction.get("group_name"),
                    instructions=[
                        Instruction(**instr)
                        for instr in instruction.get("instructions", [])
                    ],
                )
                for instruction in recipe["instructions"]
            ]
            additional_resources = []

            # Remove nutrition, instructions and ingredients from recipe
            recipe.pop("nutrition")
            recipe.pop("ingredients")
            recipe.pop("instructions")

            # Convert the prep and total into integer minutes
            recipe["prepTime"] = convert_to_minutes(recipe.get("prepTime"))
            recipe["totalTime"] = convert_to_minutes(recipe.get("totalTime"))

            transformed.append(
                Recipe(
                    **recipe,
                    nutrition=nutrition,
                    ingredients=ingredients,
                    instructions=instructions,
                    additional_resources=additional_resources,
                )
            )

        return transformed

    # Helper methods:

    def get_recipe_ids(self):
        recipe_ids = []
        page = 1
        while True:
            response = requests.get(f"{self.recipe_page_list_url}{page}")
            soup = BeautifulSoup(response.content, "html.parser")
            # Check that we have not passed the last page
            no_results = soup.find("p", class_="no-results-response")
            if no_results:
                break
            # Get the recipe ids from the page using wprm-recipe-rating class name
            recipe_classes = [
                " ".join(recipe["class"])
                for recipe in soup.find_all("div", class_="wprm-recipe-rating")
            ]
            # Extract the recipe id from the class name using regex
            ids = [re.search(r"\d+", classes).group() for classes in recipe_classes]
            recipe_ids.extend(ids)
            page += 1
            time.sleep(0.5)  # Sleep for 0.5 seconds to avoid getting blocked
        return recipe_ids

    @staticmethod
    def extract_nutrition(nutrition):
        amount, unit, name = None, None, None

        if nutrition.find("span", class_="wprm-nutrition-label-text-nutrition-value"):
            amount = nutrition.find(
                "span", class_="wprm-nutrition-label-text-nutrition-value"
            ).text

        if nutrition.find("span", class_="wprm-nutrition-label-text-nutrition-unit"):
            unit = nutrition.find(
                "span", class_="wprm-nutrition-label-text-nutrition-unit"
            ).text

        if nutrition.find("span", class_="wprm-nutrition-label-text-nutrition-label"):
            name = nutrition.find(
                "span", class_="wprm-nutrition-label-text-nutrition-label"
            ).text

        return {
            "name": name,
            "amount": amount,
            "unit": unit,
        }

    @staticmethod
    def extract_ingredient(ingredient_group):
        group_name = ingredient_group.find("h4", class_="wprm-recipe-group-name")
        group_name = group_name.text if group_name else None

        ingredients = []
        for ingredient in ingredient_group.find_all(
            "li", class_="wprm-recipe-ingredient"
        ):
            amount, unit, name, note = None, None, None, None

            if ingredient.find("span", class_="wprm-recipe-ingredient-amount"):
                amount = ingredient.find(
                    "span", class_="wprm-recipe-ingredient-amount"
                ).text

            if ingredient.find("span", class_="wprm-recipe-ingredient-unit"):
                unit = ingredient.find(
                    "span", class_="wprm-recipe-ingredient-unit"
                ).text

            if ingredient.find("span", class_="wprm-recipe-ingredient-name"):
                name = ingredient.find(
                    "span", class_="wprm-recipe-ingredient-name"
                ).text

            if ingredient.find("span", class_="wprm-recipe-ingredient-notes"):
                note = ingredient.find(
                    "span", class_="wprm-recipe-ingredient-notes"
                ).text

            ingredients.append(
                {
                    "amount": amount,
                    "unit": unit,
                    "name": name,
                    "note": note,
                }
            )
        return {
            "group_name": group_name,
            "ingredients": ingredients,
        }

    @staticmethod
    def extract_instruction(instruction_group):
        group_name = instruction_group.find("h4", class_="wprm-recipe-group-name")
        group_name = group_name.text if group_name else None

        insructions = []
        for index, instruction in enumerate(
            instruction_group.find_all("li", class_="wprm-recipe-instruction")
        ):
            text, image = None, None

            if instruction.find("div", class_="wprm-recipe-instruction-text"):
                text = instruction.find(
                    "div", class_="wprm-recipe-instruction-text"
                ).text

            if instruction.find("img"):
                image = instruction.find("img")["src"]

            insructions.append(
                {
                    "index": index,
                    "text": text,
                    "image": image,
                }
            )

        return {
            "group_name": group_name,
            "instructions": insructions,
        }
