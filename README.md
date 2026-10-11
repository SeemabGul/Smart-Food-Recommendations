# Smart Food Recommendation System

## What's new in this version

| Enhancement | Status | Where |
|---|---|---|
| User accounts with saved preferences & history | Implemented | `user_data.py`, stored locally in `users.json` |
| Allergy / ingredient-based filtering | Implemented | `recommender.py` + `food_data.csv` (`ingredients` column) + dashboard "Avoid Ingredients" field |
| Calorie chart | Implemented | `dashboard.py` -> "Show Chart" button (needs `matplotlib`) |
| Real nutrition API integration | Extension point ready | `recommender.py` -> `fetch_from_external_api()` - requires your own API key from a provider like Edamam or Spoonacular |
| Standalone installer (.exe) | Instructions below | Build it yourself with PyInstaller on your own Windows PC |

## Setup

1. Make sure Python 3.10+ is installed.
2. Open this folder in PyCharm.
3. Install the one extra dependency (only matplotlib is needed beyond the standard library):
   ```
   pip install -r requirements.txt
   ```
4. Run `main.py`.

## How saved data works

The first time a username logs in, a record is created for them in `users.json`
(auto-generated in the same folder). Every time "Get Recommendations" is
clicked, their diet type, calorie limit, and allergy list are saved - so next
time they log in, the form is pre-filled with their last settings. Every
search is also logged to their history, viewable via "View History" in the
dashboard.

## Building a standalone .exe installer (optional)

This has to be done on your own Windows machine:

```
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "food_data.csv;." main.py
```

The `.exe` will appear in the `dist` folder.

## Adding a real nutrition API (optional)

1. Sign up with a provider (Edamam, Spoonacular, or USDA FoodData Central).
2. `pip install requests`
3. Fill in `fetch_from_external_api()` in `recommender.py` using your API key.
4. Merge its results into `get_recommendations()` alongside the local CSV data.
