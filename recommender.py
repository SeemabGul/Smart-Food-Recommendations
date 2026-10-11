import csv
import os

CSV_PATH = os.path.join(os.path.dirname(__file__), "food_data.csv")


def load_food_data():
    foods = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["calories"] = int(row["calories"])
            row["ingredients"] = [
                i.strip().lower() for i in row.get("ingredients", "").split(";") if i.strip()
            ]
            foods.append(row)
    return foods


def get_recommendations(diet_type="Any", max_calories=1000, exclude_allergens=None):
    """
    diet_type: "Any", "Vegetarian", "Vegan", or "Non-Vegetarian"
    max_calories: upper limit per food item
    exclude_allergens: list of ingredient/allergen keywords to avoid,
                        e.g. ["dairy", "nuts", "egg"]
    """
    exclude_allergens = [a.strip().lower() for a in (exclude_allergens or []) if a.strip()]
    foods = load_food_data()
    results = []

    for food in foods:
        if food["calories"] > max_calories:
            continue
        if diet_type != "Any" and food["diet_type"].lower() != diet_type.lower():
            continue
        if exclude_allergens and any(a in food["ingredients"] for a in exclude_allergens):
            continue
        results.append(food)

    return results


def fetch_from_external_api(query):
    """
    Extension point for a real nutrition API (e.g. Edamam, Spoonacular, USDA
    FoodData Central). To enable it:

      1. Sign up with a provider and get an API key.
      2. pip install requests
      3. Implement the request below using your key, and merge/replace the
         local CSV results with the API response in get_recommendations().

    Left unimplemented on purpose since it requires a personal API key
    that only you can provide.
    """
    raise NotImplementedError(
        "Connect a real nutrition API here using your own API key."
    )
