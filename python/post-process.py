import json
import os
from datetime import date
from pathlib import Path

import requests
from dotenv import find_dotenv, load_dotenv

DATA_DIR = Path(__file__).parent.resolve() / ".." / "data"


def load_json_data(filename):
    """Load JSON data from the data folder."""

    # Load the JSON data
    path = DATA_DIR / filename
    with path.open("r") as f:
        data = json.load(f)

    # Return a dict
    return {d["identifier"]: d for d in data}


def main():

    # Load the meal plan
    meal_plan = load_json_data("meal-plan.json")
    meal_plan_labels = load_json_data("meal-plan-labels.json")

    # Load the recipes
    recipes = load_json_data("recipes.json")

    # Trim to today
    today = date.today().strftime("%Y-%m-%d")
    today_meals = list(filter(lambda d: d["date"] == today, meal_plan.values()))

    # Trim to dinner only
    dinner_meals = [
        meal
        for meal in today_meals
        if meal_plan_labels[meal["labelId"]]["name"] == "Dinner"
    ]

    # We have dinner plan for today
    if len(dinner_meals) > 0:

        # Get meal names
        meal_names = [recipes[meal["recipeId"]]["name"] for meal in dinner_meals]

        if len(meal_names) == 1:
            meal_names_str = meal_names[0]
        elif len(meal_names) == 2:
            meal_names_str = f"{meal_names[0]} and {meal_names[1]}"
        else:
            meal_names_str = ", ".join(meal_names[:-1]) + f", and {meal_names[-1]}"

        # Construct the message
        message = f"Tonight you're having {meal_names_str} for dinner 🐷 🍽"
    else:
        message = "You don't yet have a dinner plan for today 🙁"

    # Get the webhook URL
    webhook_url = os.getenv("SEND_DINNER_WEBHOOK_URL")
    if webhook_url is None:
        raise ValueError("Please define 'SEND_DINNER_WEBHOOK_URL' environment variable")

    # Send the push notification with the message
    requests.post(webhook_url, params={"message": message})


if __name__ == "__main__":

    # Load the .env file
    load_dotenv(find_dotenv())

    # Run
    main()
