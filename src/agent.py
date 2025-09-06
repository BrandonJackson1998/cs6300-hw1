#!/usr/bin/env python3

import os
from smolagents import CodeAgent, OpenAIServerModel
from tools import NutritionLookup
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Initialize tools
nutrition_tool = NutritionLookup()
tools = [nutrition_tool]

# Initialize model
model_id = "gemini-2.5-flash"
model = OpenAIServerModel(
    model_id=model_id,
    api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY"),
)

# Initialize agent
agent = CodeAgent(
    tools=tools,
    model=model,
    additional_authorized_imports=[],
    max_steps=6
)

def main():
    # Ask for valid age
    while True:
        age = input("Enter your age: ").strip()
        if not age.isdigit() or int(age) <= 0:
            print("Invalid age. Please enter a positive integer.")
            continue
        break
    # Ask for valid gender
    while True:
        gender = input("Enter your gender(male or female): ").strip()
        if gender.lower() not in ["male", "female"]:
            print("Invalid gender. Please enter 'male' or 'female'.")
            continue
        break

    # Collect food items
    todays_food = []
    print("\nEnter each food item you ate today one at a time (type 'done' when finished):")
    while True:
        food_item = input("> ").strip()
        if food_item.lower() == "done":
            break
        if food_item:
            todays_food.append(food_item)

    # If no food was eaten, exit
    if not todays_food:
        print("No food items entered. Exiting.")
        return

    # Build query
    query = (
        f"Here is everything I ate and drank today as a {age} year old {gender}: "
        + "; ".join(todays_food)
        + ".\n"
        + "Please provide estimated calories, check for any macro/micro deficits/excesses."
    )

    # Run the agent with the query
    answer = agent.run(query)
    print("\nNutrition Agent Output:\n", answer)


if __name__ == "__main__":
    main()
