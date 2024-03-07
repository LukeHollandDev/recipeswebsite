# HelloFreshed 2 - Recipe Scraper

This directory contains the application which will perform the scraping of recipes, it stores the recipes in the `recipes` directory.

### Technology

* Python 3
  * Requests
* Black formatter for Python 3
  * https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter

### Usage

Create a Python virtual environment:

```bash
python -m venv env
```

Activate the virtual environment (Powershell, Git Bash (windows), Bash/Zsh (unix)):

```bash
./env/Scripts/activate
```

```bash
source ./env/Scripts/activate
```

```bash
source ./env/bin/activate
```

Install all the dependencies:

```bash
pip install -r requirements.txt
```

Run the script, specifying the output location, config to use:

```bash
python main.py --output "../recipes" --config "hellofresh"
```

Once executed the script will show the progress in the terminal / command prompt and then will store the recipes inside of the output directory provided in the command. They will be stored in the in a directory named the same as the config used.

The code will automatically check for duplicates if any exists and will only store new recipes.

### Available Configurations

* `hellofresh`
* `justonecookbook`

### Recipe Data Model

The model can be found in the Pydantic model file: `models/Recipe.py`.

This is the structure the configurations use to structure their recipes before storing them in the file.

You can find examples of these recipe files inside of `recipes` directory.