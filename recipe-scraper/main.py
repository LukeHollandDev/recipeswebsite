# Write playwright code to visit a website in headless mode and print the local storage data
import asyncio, argparse, json, os
from config import Configurations

# Create arg parser to parse --output and --config options
parser = argparse.ArgumentParser(description="Recipe Generator")
parser.add_argument(
    "-o",
    "--output",
    metavar="FILEPATH",
    help="Path to the directory to store the output recipes",
    required=True,
)
parser.add_argument(
    "-c",
    "--config",
    choices=["hellofresh", "justonecookbook"],
    help="Choose config for recipe scraping",
    required=True,
)


async def main():
    args = parser.parse_args()
    config, output_directory = args.config, args.output

    # Load the config from the config module
    scraper = Configurations.get(config)
    if not scraper:
        print(f"Config {config} not found")
        return

    print(f"Loaded config {scraper.name}")

    # If the scraper requires a bearer token, set it using the set_bearer_token method
    if scraper.bearer_required:
        print("Setting bearer (authorisation) token")
        await scraper.set_bearer_token()

    # Scrape the recipes and save them to the output directory
    print("Scraping recipes")
    recipes = scraper.get_recipes()
    os.makedirs(f"{output_directory}/{config}", exist_ok=True)
    with open(f"{output_directory}/{config}/raw.json", "w") as file:
        print(f"Saving raw recipe data to {output_directory}/{config}/raw.json")
        file.write(json.dumps(recipes, indent=2))

    # # Load the recipes from the output directory and count unique recipes
    # with open(f"{output_directory}/{config}/raw.json", "r") as file:
    #     recipes = json.load(file)

    # Get unique recipes using their id attribute
    unique_recipes = list({recipe.get("id"): recipe for recipe in recipes}.values())

    print(f"Scraped {len(unique_recipes)} unique recipes")

    # Convert recipes into standard format and save them to the output directory
    transformed_recipes = scraper.transform_recipes(unique_recipes)
    transformed_recipes = [recipe.dict() for recipe in transformed_recipes if recipe]
    with open(f"{output_directory}/{config}/recipes.json", "w") as file:
        file.write(json.dumps(transformed_recipes, indent=2))

    print(f"Saved transformed recipes: {output_directory}/{config}/recipes.json")


if __name__ == "__main__":
    asyncio.run(main())
