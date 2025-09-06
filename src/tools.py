#!/usr/bin/env python3
import os
import requests
from smolagents import Tool

class NutritionLookup(Tool):
    """
    A tool that uses the Nutritionix API to fetch detailed nutrition information about food items.
    """

    name: str = "nutrition_lookup"
    description: str = (
        "Get detailed nutrition facts for a given food item. "
        "Returns calories, protein, carbs, fat, and other key nutrients."
    )
    inputs: dict = {
        "food": {
            "type": "string",
            "description": "Name of the food item (e.g., '1 cup mashed potatoes and 2 tbsp gravy').",
        }
    }
    output_type: str = "string"

    def __init__(self):
        super().__init__()
        self.app_id = os.getenv("NUTRITIONIX_APP_ID")
        self.app_key = os.getenv("NUTRITIONIX_API_KEY")
        if not self.app_id or not self.app_key:
            raise ValueError("Missing NUTRITIONIX_APP_ID or NUTRITIONIX_API_KEY in environment variables.")

    def forward(self, food: str) -> str:
        """
        Calls Nutritionix Natural Language Nutrients API to get nutrition info.

        Args:
            food: The description of the food item(s).

        Returns:
            A string with nutrition data (calories, protein, carbs, fat).
        """
        if not isinstance(food, str):
            raise ValueError("`food` must be a string.")
        if not food.strip():
            raise ValueError("`food` cannot be an empty string.")

        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.app_key,
            "Content-Type": "application/json",
        }
        payload = {"query": food}

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Nutritionix API error: {response.status_code} - {response.text}")

        data = response.json()

        # Extract the first food item from the response
        foods = data.get("foods", [])
        if not foods:
            return f"No nutrition data found for {food}."

        results = []
        for item in foods:
            name = item.get("food_name", "Unknown")
            calories = item.get("nf_calories", "N/A")
            protein = item.get("nf_protein", "N/A")
            carbs = item.get("nf_total_carbohydrate", "N/A")
            fat = item.get("nf_total_fat", "N/A")
            serving = f"{item.get('serving_qty', '')} {item.get('serving_unit', '')}".strip()

            results.append(
                f"{name.title()} ({serving}): {calories} kcal, "
                f"Protein: {protein} g, Carbs: {carbs} g, Fat: {fat} g"
            )

        return "\n".join(results)
    