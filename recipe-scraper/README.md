# HelloFreshed 2 - Recipe Scraper

This directory contains the application which will perform the scraping of recipes, it stores the recipes in the `recipes` directory.

### Technology

* Python 3
  * Requests

### Usage

Create a Python virtual environment:

```bash
python -m venv env
```

Install all the dependencies:

```bash
pip install -r requirements.txt
```

Run the script, specifying the output location and which config to use:

```bash
python main.py --output "../recipes" --config "hellofresh"
```

Once executed the script will show the progress in the terminal / command prompt and then will store the recipes inside of the output directory provided in the command. They will be stored in the in a directory named the same as the config used.

The code will automatically check for duplicates if any exists and will only store new recipes.

### Available Configurations

* `hellofresh`