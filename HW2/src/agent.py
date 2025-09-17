#!/usr/bin/env python3

import os
from datetime import date
import dotenv
from smolagents import CodeAgent, OpenAIServerModel

from tools import NutritionLookup, UserTracker, DeficitCalculator, UserTrends, ReportGenerator

# Load environment variables
dotenv.load_dotenv()

# Initialize model
model_id = "gemini-2.5-flash"
model = OpenAIServerModel(
    model_id=model_id,
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)

# Initialize tools
nutrition_tool = NutritionLookup()
user_tracker = UserTracker()
deficit_tool = DeficitCalculator()
trends_tool = UserTrends(model=model)
report_tool = ReportGenerator()
tools = [
    nutrition_tool,
    user_tracker,
    deficit_tool,
    trends_tool,
    report_tool,
]

# Initialize agent
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=["json"],
    max_steps=15
)


def main():
    print("👋 Welcome to Nutrition Agent!\n")

    current_user = ""
    while current_user.lower() not in ["y", "n"]:
        current_user = input("Are you a returning user? (y/n): ").strip().lower()

    if current_user == "y":

        print("Welcome back! We'll retrieve your previous data.")
    else:
        print("Let's set up your profile.")

    # Collect user info
    name = input("Enter your name: ").strip()
    if current_user == "y":
        user_file_path = os.path.join(os.path.dirname(__file__), "../data", f"{name.lower()}.json")
        if not os.path.isfile(user_file_path):
            print(f"⚠️ No data found for user '{name}'. Please set up your profile as a new user.")
            current_user = "n"
    if current_user == "n":
        age = int(input("Enter your age: ").strip())
        weight = float(input("Enter your weight (kg): ").strip())
        height = float(input("Enter your height (cm): ").strip())
        gender = ""
        while gender.lower() not in ["male", "female"]:
            gender = input("Enter your gender (male/female): ").strip()

    # Ask for date (defaults to today if blank)
    user_date = input(f"Enter the date for this log [default: {date.today()}]: ").strip()
    if not user_date:
        user_date = str(date.today())

    # Collect foods
    todays_food = []
    print("\nEnter each food item you ate today one at a time (type 'done' when finished):")
    while True:
        food_item = input("> ").strip()
        if food_item.lower() == "done":
            break
        if food_item:
            todays_food.append(food_item)

    if not todays_food:
        print("⚠️ No food items entered. Exiting.")
        return

    if current_user == "y":
        query = (
            f"User: {name}. "
            f"Date: {user_date}. "
            f"Food eaten: {', '.join(todays_food)}.\n"
            "Find the user and estimate calories, check for macro/micro deficits or surpluses, "
            "and provide suggestions."
        )
    else:
        query = (
            f"User: {name}, {age} years old {gender}, {weight}kg, {height}cm. "
            f"Date: {user_date}. "
            f"Food eaten: {', '.join(todays_food)}.\n"
            "Create the user and estimate calories, check for macro/micro deficits or surpluses, "
            "and provide suggestions."
        )

    # Run the agent
    answer = agent.run(query)

    print("\n📊 Nutrition Agent Output:\n")
    print(answer)


if __name__ == "__main__":
    main()
