#!/usr/bin/env python3
import os
import json
import requests
from smolagents import Tool
from datetime import date

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------
# 1. Nutrition Lookup
# -----------------------------
class NutritionLookup(Tool):
    """
    A tool that uses the Nutritionix API to fetch detailed nutrition information
    about food items and logs results into the user's JSON file.
    """

    name: str = "nutrition_lookup"
    description: str = (
        "Get detailed nutrition facts for a list of food items. "
        "Returns summed up calories, protein, carbs, and fat data. "
        "Given a user name and a date, if it's a previous user and a new date for the user, appends to user history, else if duplicate date, replaces the existing log, else creates a new log."
    )
    inputs: dict = {
        "food": {
            "type": "array",
            "items": {"type": "string", "description": "Name of food item"},
            "description": "List of food item(s).",
        },
        "name": {
            "type": "string",
            "description": "User’s name to log into their file.",
        },
        "log_date": {
            "type": "string",
            "description": "Date string (YYYY-MM-DD) for today’s entry.",
        },
    }
    output_type: str = "string"

    def __init__(self):
        super().__init__()
        self.app_id = os.getenv("NUTRITIONIX_APP_ID")
        self.app_key = os.getenv("NUTRITIONIX_API_KEY")
        if not self.app_id or not self.app_key:
            raise ValueError("Missing NUTRITIONIX_APP_ID or NUTRITIONIX_API_KEY.")

    def forward(self, food: list[str], name: str, log_date: str) -> dict:
        if not isinstance(food, list) or not food or not all(isinstance(f, str) and f.strip() for f in food):
            raise ValueError("`food` must be a non-empty list of non-empty strings.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("`name` must be a non-empty string.")
        if not isinstance(log_date, str) or not log_date.strip():
            raise ValueError("`log_date` must be a non-empty string.")

        url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.app_key,
            "Content-Type": "application/json",
        }
        payload = {"query": ", ".join(food)}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise RuntimeError(f"Nutritionix API error: {response.status_code} - {response.text}")

        data = response.json().get("foods", [])
        totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        foods_logged = []

        for item in data:
            totals["calories"] += item.get("nf_calories", 0) or 0
            totals["protein"] += item.get("nf_protein", 0) or 0
            totals["carbs"] += item.get("nf_total_carbohydrate", 0) or 0
            totals["fat"] += item.get("nf_total_fat", 0) or 0
            foods_logged.append(item.get("food_name", "Unknown"))

        # Save into user file
        filepath = os.path.join(DATA_DIR, f"{name.lower()}.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                user_data = json.load(f)
        else:
            user_data = {"name": name, "history": []}

        # Find today’s entry
        today_entry = next((h for h in user_data["history"] if h["date"] == log_date), None)
        if not today_entry:
            today_entry = {"date": log_date, "foods": [], "totals": {}, "analysis": {}}
            user_data["history"].append(today_entry)

        today_entry["foods"].extend(foods_logged)
        today_entry["totals"] = totals

        with open(filepath, "w") as f:
            json.dump(user_data, f, indent=2)

        return {"foods": foods_logged, "totals": totals}

# -----------------------------
# 2. User Tracker
# -----------------------------
class UserTracker(Tool):
    """
    A tool to save and retrieve user nutrition data.
    Stores data in HW2/data/{username}.json
    """

    name: str = "user_tracker"
    description: str = "Save or retrieve user info (name, age, weight, height, gender, food history)."
    inputs: dict = {
        "data": {
            "type": "object",
            "description": "User data, daily intake, and nutrition totals.",
        },
        "action": {
            "type": "string",
            "description": "Action to perform: save or retrieve user data.",
        }
    }
    output_type: str = "string"

    def __init__(self, data_dir="HW2/data"):
        super().__init__()
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)

    def forward(self, data: dict, action: str) -> str:
        """
        Save, retrieve, or update user data in a JSON file.
        """
        if action is None:
            return "No action provided. Please specify 'save' or 'retrieve'."
        if not isinstance(action, str):
            return "Invalid action type. Must be a string."
        action = action.strip().lower()
        if action not in {"save", "retrieve"}:
            return "Invalid action. Must be one of: save, retrieve."
        if action == "save" and data is None:
            return "No user data provided."

        required = ["name"]
        for r in required:
            if r not in data:
                return f"Missing required field: {r}"

        username = data["name"].strip().lower()
        filepath = os.path.join(self.data_dir, f"{username}.json")

        # Load existing data if file exists
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                user_data = json.load(f)
        else:
            user_data = {
                "name": data["name"],
                "age": data["age"],
                "weight": data["weight"],
                "height": data["height"],
                "gender": data["gender"],
                "history": []
            }
        if action == "retrieve":
            return json.dumps(user_data, indent=2)

        if action == "save":
            # Update demographics if changed
            for field in ["age", "weight", "height", "gender"]:
                if field in data and data[field] != user_data.get(field):
                    user_data[field] = data[field]
            
            # Merge today's foods and totals if date matches
            today_str = str(date.today())
            today_entry = next((h for h in user_data["history"] if h.get("date") == today_str), None)
            if today_entry:
                # Update existing entry for today
                if "foods" in data:
                    today_entry["foods"].extend(data.get("foods", []))
                if "totals" in data:
                    today_entry["totals"] = data.get("totals", {})
            else:
                # No entry for today, append a new one if data provided
                if "foods" in data or "totals" in data:
                    entry = {
                        "date": str(date.today()),
                        "foods": data.get("foods", []),
                        "totals": data.get("totals", {}),
                    }
                    user_data["history"].append(entry)
                # Save back to file
                with open(filepath, "w") as f:
                    json.dump(user_data, f, indent=2)

            return f"User data saved for {data['name']} in {filepath}"

# -----------------------------
# 3. User Trends
# -----------------------------
class UserTrends(Tool):
    """
    A tool to analyze user nutrition trends across multiple days.
    """

    name: str = "user_trends"
    description: str = "Given a user, if the user has more than 1 date of history, analyze historical nutrition data for long-term trends."
    inputs: dict = {
        "user": {
            "type": "string",
            "description": "User's name for checking trends",
        }
    }
    output_type: str = "string"

    def __init__(self, model):
        super().__init__(
            name=self.name,
            description=self.description,
            output_type=self.output_type,
            inputs=self.inputs,
        )
        self.model = model  # Pass in Gemini/OpenAI model
        
    def forward(self, user: str) -> str:
        if not user:
            return "No user name provided."

        filepath = os.path.join(DATA_DIR, f"{user.lower()}.json")
        if not os.path.exists(filepath):
            return f"No data found for user {user}."

        with open(filepath, "r") as f:
            user_data = json.load(f)

        history = user_data.get("history", [])
        if len(history) < 2:
            return "Not enough history to analyze trends."

        # Extract daily totals for analysis
        daily_totals = []
        for entry in history:
            totals = entry.get("totals", {})
            daily_totals.append({
                "calories": float(totals.get("calories", 0)),
                "protein": float(totals.get("protein", 0)),
                "carbs": float(totals.get("carbs", 0)),
                "fat": float(totals.get("fat", 0)),
            })

        calorie_vals = [day["calories"] for day in daily_totals]
        protein_vals = [day["protein"] for day in daily_totals]
        carb_vals = [day["carbs"] for day in daily_totals]
        fat_vals = [day["fat"] for day in daily_totals]

        def avg(values): return sum(values) / len(values) if values else 0

        stats = {
            "calories": {"avg": avg(calorie_vals), "min": min(calorie_vals), "max": max(calorie_vals)},
            "protein": {"avg": avg(protein_vals), "min": min(protein_vals), "max": max(protein_vals)},
            "carbs": {"avg": avg(carb_vals), "min": min(carb_vals), "max": max(carb_vals)},
            "fat": {"avg": avg(fat_vals), "min": min(fat_vals), "max": max(fat_vals)},
        }

        # Build summary
        summary = (
            f"Over the past {len(history)} days:\n"
            f"- Calories averaged {stats['calories']['avg']:.0f} kcal/day "
            f"(range {stats['calories']['min']}–{stats['calories']['max']}).\n"
            f"- Protein averaged {stats['protein']['avg']:.1f} g/day "
            f"(range {stats['protein']['min']}–{stats['protein']['max']}).\n"
            f"- Carbs averaged {stats['carbs']['avg']:.1f} g/day "
            f"(range {stats['carbs']['min']}–{stats['carbs']['max']}).\n"
            f"- Fat averaged {stats['fat']['avg']:.1f} g/day "
            f"(range {stats['fat']['min']}–{stats['fat']['max']}).\n\n"
        )

        # Prompt Gemini for a summary
        prompt = (
            "You are a nutrition assistant. Based on these statistics and user data, write a concise summary "
            "of the user's nutrition trends in 3 sentences or less. Be specific but encouraging.\n\n"
            f"User: {json.dumps(user_data, indent=2)}\n"
            f"Stats: {json.dumps(stats, indent=2)}\n"
            f"Days tracked: {len(history)}"
        )

        response = self.model([
            {"role": "system", "content": "You are a helpful nutrition assistant."},
            {"role": "user", "content": prompt},
        ])

        # If it's a ChatMessage object, grab the content
        if hasattr(response, "content"):
            return summary + response.content
        elif isinstance(response, dict) and "content" in response:
            return summary + response["content"]
        elif isinstance(response, str):
            return summary + response
        else:
            return summary + str(response)

# -----------------------------
# 4. Deficit Calculator
# -----------------------------
class DeficitCalculator(Tool):
    """
    A tool that evaluates deficits/surpluses against rough daily guidelines
    and logs them into the user’s file.
    """

    name: str = "deficit_calculator"
    description: str = "Check nutrition totals against guidelines and log analysis."
    inputs: dict = {
        "totals": {"type": "object", "description": "Totals dict of nutrition values."},
        "user_info": {"type": "array", "description": "User personal data for context."},
        "log_date": {"type": "string", "description": "Date for today’s entry."},
    }
    output_type: str = "string"

    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description,
            output_type=self.output_type,
            inputs=self.inputs,
        )

    def forward(self, totals: dict, user_info: list, log_date: str) -> dict:
        if totals is None:
            raise ValueError("`totals` must be provided and be a dict.")
        if not isinstance(totals, dict):
            raise ValueError("`totals` must be a dict.")
        if not log_date:
            raise ValueError("`log_date` must be provided.")
        if not user_info or not isinstance(user_info, list) or len(user_info) < 5:
            raise ValueError("`user_info` must be a list with at least 5 elements: name, age, weight, height, gender.")

        name, age, weight, height, gender = user_info

        # --- Personalized guideline estimation ---
        # Basal Metabolic Rate (Mifflin-St Jeor Equation)
        if gender.lower() == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        # Assume sedentary activity factor (1.2)
        calories_target = round(bmr * 1.2)

        # Protein target (0.8 g per kg body weight)
        protein_target = round(weight * 0.8)

        # Carb target (45–65% calories → use ~55%)
        carbs_target = round((calories_target * 0.55) / 4)

        # Fat target (25–35% calories → use ~30%)
        fat_target = round((calories_target * 0.3) / 9)

        guidelines = {
            "calories": calories_target,
            "protein": protein_target,
            "carbs": carbs_target,
            "fat": fat_target,
        }

        # --- Compare actual totals vs targets ---
        analysis = {}
        for k, target in guidelines.items():
            actual = float(totals.get(k, 0))
            if actual < target * 0.9:
                analysis[k] = f"Deficit: {actual:.1f} vs {target}"
            elif actual > target * 1.1:
                analysis[k] = f"Surplus: {actual:.1f} vs {target}"
            else:
                analysis[k] = f"Balanced: {actual:.1f} vs {target}"

        # --- Save into user file ---
        filepath = os.path.join(DATA_DIR, f"{name.lower()}.json")
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                user_data = json.load(f)
        else:
            raise FileNotFoundError(f"No data file found for {name}")

        today_entry = next((h for h in user_data["history"] if h["date"] == log_date), None)
        if not today_entry:
            today_entry = {"date": log_date, "foods": [], "totals": {}, "analysis": {}}
            user_data["history"].append(today_entry)

        today_entry["analysis"] = analysis
        with open(filepath, "w") as f:
            json.dump(user_data, f, indent=2)

        return analysis

# -----------------------------
# 5. Report Generator
# -----------------------------
class ReportGenerator(Tool):
    """
    A tool to generate a formatted nutrition report from multiple components.
    """

    name: str = "report_generator"
    description: str = "Generate a full nutrition report with totals, deficits, and trends. With any errors logged at the end."
    inputs: dict = {
        "user_info": {
            "type": "array",
            "description": "User personal data: [Name, Age, Weight, Height, Gender]",
        },
        "totals": {
            "type": "object",
            "description": "Daily nutrition totals (calories, macros).",
        },
        "deficits": {
            "type": "string",
            "description": "Deficit/surplus analysis results.",
        },
        "trends": {
            "type": "string",
            "description": "User trend insights.",
        },
        "errors": {
            "type": "string",
            "description": "Any unexpected results encountered during report generation.",
            "nullable": True
        }
    }
    output_type: str = "string"

    def forward(self, user_info, totals, deficits, trends, errors=None) -> str:
        report = ["--- Nutrition Report ---"]

        if user_info and isinstance(user_info, (list, tuple)) and len(user_info) == 5:
            name, age, weight, height, gender = user_info
            user_info_str = f"Name: {name}, Age: {age}, Weight: {weight} kg, Height: {height} cm, Gender: {gender}"
            report.append(f"User Info: {user_info_str}")
        if totals:
            report.append(f"Daily Totals: {totals}")
        if deficits:
            report.append(f"Deficits/Surpluses:\n{deficits}")
        if trends:
            report.append(f"Long-Term Trends:\n{trends}")
        if errors:
            report.append(f"Errors:\n{errors}")
        return "\n".join(report)
