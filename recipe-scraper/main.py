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

    print(f"Loaded config {scraper.get_name()}")

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
        file.write(json.dumps(recipes, indent=4))

    # # Load the recipes from the output directory and count unique recipes
    # with open(f"{output_directory}/{config}/raw.json", "r") as file:
    #     recipes = json.load(file)

    # Get unique recipes using their id attribute
    unique_recipes = {recipe.get("id"): recipe for recipe in recipes}.values()

    print(f"Scraped {len(unique_recipes)} unique recipes")

    # Convert recipes into standard format and save them to the output directory
    # TODO: Implement this part


if __name__ == "__main__":
    asyncio.run(main())
