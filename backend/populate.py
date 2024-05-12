import os, json, time, random
from sqlmodel import create_engine, Session

from models import Recipe, Nutrient, Ingredient, Instruction, Resource

# Combine recipes from "recipes" directory and store in array
recipes = []
for root, _, files in os.walk("recipes"):
    for file in files:
        if file == "recipes.json":
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                data = json.load(f)
                recipes.extend(data)

# Randomise the recipes
random.shuffle(recipes)

# Get the database URL from the environment variable
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    print("DATABASE_URL is not set.")
    exit(0)

# Create the database engine
engine = create_engine(database_url)

# Get time started, so can get total time at the end
start_time = time.time()

# Create a session
with Session(engine) as session:
    recipe_count = len(recipes)
    # Iterate over the data and insert it into the database
    for i, recipe in enumerate(recipes):
        # Show the progress
        print(f"{i + 1} / {recipe_count}", end="\r")

        # Create recipe and commit so id is available
        recipe_model = Recipe.Recipe(
            id_other=recipe.get("id"),
            title=recipe.get("title"),
            description=recipe.get("description"),
            url=recipe.get("url"),
            image=recipe.get("image"),
            cuisine=recipe.get("cuisine"),
            prepTime=recipe.get("prepTime"),
            totalTime=recipe.get("totalTime"),
            servings=recipe.get("servings"),
        )
        session.add(recipe_model)
        session.commit()
        recipe_id = recipe_model.id

        # Create ingredients
        for group in recipe.get("ingredients", []):
            group_model = Ingredient.IngredientGroup(
                name=group.get("name"), recipe_id=recipe_id
            )
            session.add(group_model)
            session.commit()
            group_id = group_model.id
            for ingredient in group.get("ingredients", []):
                session.add(
                    Ingredient.Ingredient(
                        name=ingredient.get("name"),
                        amount_lower=ingredient.get("amount_lower"),
                        amount_upper=ingredient.get("amount_upper"),
                        unit=ingredient.get("unit"),
                        note=ingredient.get("note"),
                        group_id=group_id,
                    )
                )

        # Create instructions
        for group in recipe.get("instructions", []):
            group_model = Instruction.InstructionGroup(
                name=group.get("name"), recipe_id=recipe_id
            )
            session.add(group_model)
            session.commit()
            group_id = group_model.id
            for instruction in group.get("instructions", []):
                session.add(
                    Instruction.Instruction(
                        index=instruction.get("index"),
                        text=instruction.get("text"),
                        image=instruction.get("image"),
                        group_id=group_id,
                    )
                )

        # Create nutriants
        for nutrient in recipe.get("nutrition", []):
            session.add(
                Nutrient.Nutrient(
                    name=nutrient.get("name"),
                    amount=nutrient.get("amount"),
                    unit=nutrient.get("unit"),
                    recipe_id=recipe_id,
                )
            )

        # Create resources
        for resource in recipe.get("additional_resources", []):
            session.add(
                Resource.Resource(
                    name=resource.get("name"),
                    type=resource.get("type"),
                    value=resource.get("value"),
                    recipe_id=recipe_id,
                )
            )

        # Commit the changes
        session.commit()

    # Reset print, by printing final progress bar
    print(f"Recipe: {recipe_count} / {recipe_count}")

# Calculate and print the total time taken
total_time = time.time() - start_time
minutes = int(total_time // 60)
seconds = int(total_time % 60)
print(f"Total time taken: {minutes} minutes and {seconds} seconds")
