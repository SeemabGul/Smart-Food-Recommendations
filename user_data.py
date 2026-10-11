"""
Handles saving user preferences and search history to a local JSON file
(users.json), so returning users see their past choices and searches.
No internet or database server needed.
"""

import json
import os
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), "users.json")


def _load_all():
    if not os.path.exists(DATA_PATH):
        return {}
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save_all(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_user(username):
    """Returns the user's saved record, creating one on first login."""
    data = _load_all()
    if username not in data:
        data[username] = {
            "preferences": {"diet_type": "Any", "max_calories": 500, "allergies": []},
            "history": []
        }
        _save_all(data)
    return data[username]


def save_preferences(username, diet_type, max_calories, allergies):
    data = _load_all()
    user = data.setdefault(username, {"preferences": {}, "history": []})
    user["preferences"] = {
        "diet_type": diet_type,
        "max_calories": max_calories,
        "allergies": allergies
    }
    _save_all(data)


def add_history_entry(username, results):
    data = _load_all()
    user = data.setdefault(username, {"preferences": {}, "history": []})
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(results),
        "foods": [r["food_name"] for r in results][:10]
    }
    user["history"].insert(0, entry)
    user["history"] = user["history"][:20]  # keep last 20 searches
    _save_all(data)


def get_history(username):
    data = _load_all()
    return data.get(username, {}).get("history", [])
