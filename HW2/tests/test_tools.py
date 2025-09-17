#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# tests/test_tools.py
import os
import json
import pytest
from unittest.mock import patch, MagicMock
from datetime import date

from tools import (
    NutritionLookup,
    UserTracker,
    UserTrends,
    DeficitCalculator,
    ReportGenerator,
    DATA_DIR
)


# ------------------------------------------
# 1. NutritionLookup
# ------------------------------------------
@patch("tools.requests.post")
def test_nutrition_lookup_success(mock_post):
    # Mock API response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "foods": [
            {"food_name": "apple", "nf_calories": 95, "nf_protein": 0.5, "nf_total_carbohydrate": 25, "nf_total_fat": 0.3}
        ]
    }

    tool = NutritionLookup()
    log_date = str(date.today())
    result = tool.forward(["apple"], "TestUser", log_date)

    assert "foods" in result
    assert "totals" in result
    assert result["totals"]["calories"] == 95

    # Ensure file is created
    filepath = os.path.join(DATA_DIR, "testuser.json")
    with open(filepath, "r") as f:
        user_data = json.load(f)
    assert user_data["history"][0]["totals"]["calories"] == 95


# ------------------------------------------
# 2. UserTracker
# ------------------------------------------
def test_user_tracker_save_and_retrieve(tmp_path):
    tool = UserTracker(data_dir=tmp_path)

    data = {
        "name": "Alice",
        "age": 30,
        "weight": 60,
        "height": 165,
        "gender": "female",
        "foods": ["banana"],
        "totals": {"calories": 100}
    }

    save_msg = tool.forward(data, "save")
    assert "User data saved" in save_msg

    retrieved = tool.forward({"name": "Alice"}, "retrieve")
    retrieved_json = json.loads(retrieved)
    assert retrieved_json["name"] == "Alice"
    assert "history" in retrieved_json


# ------------------------------------------
# 3. UserTrends
# ------------------------------------------
def test_user_trends_with_mock_model():
    # Create mock user data file with history
    user_file = os.path.join(DATA_DIR, "bob.json")
    user_data = {
        "name": "Bob",
        "history": [
            {"date": "2025-09-14", "totals": {"calories": 2000, "protein": 50, "carbs": 250, "fat": 60}},
            {"date": "2025-09-15", "totals": {"calories": 2200, "protein": 55, "carbs": 270, "fat": 65}},
        ],
    }
    with open(user_file, "w") as f:
        json.dump(user_data, f)

    # Mock Gemini model
    mock_model = MagicMock(return_value="Bob’s intake is fairly balanced with slight increases in carbs and protein.")
    tool = UserTrends(model=mock_model)

    result = tool.forward("Bob")
    assert "Over the past 2 days:" in result
    assert "Bob’s intake is fairly balanced" in result


# ------------------------------------------
# 4. DeficitCalculator
# ------------------------------------------
def test_deficit_calculator_creates_analysis(tmp_path):
    # Create user file with empty history
    user_file = os.path.join(DATA_DIR, "carol.json")
    user_data = {"name": "Carol", "history": []}
    with open(user_file, "w") as f:
        json.dump(user_data, f)

    tool = DeficitCalculator()
    totals = {"calories": 1500, "protein": 40, "carbs": 100, "fat": 30}
    user_info = ["Carol", 25, 55, 160, "female"]
    log_date = str(date.today())

    analysis = tool.forward(totals, user_info, log_date)

    assert "calories" in analysis
    assert any("Deficit" in v or "Surplus" in v for v in analysis.values())

    # File should now include analysis
    with open(user_file, "r") as f:
        saved = json.load(f)
    assert "analysis" in saved["history"][0]


# ------------------------------------------
# 5. ReportGenerator
# ------------------------------------------
def test_report_generator_basic():
    tool = ReportGenerator()
    user_info = ["Dave", 40, 80, 175, "male"]
    totals = {"calories": 2000, "protein": 70}
    deficits = "Protein balanced, calories slightly low."
    trends = "Over 5 days, stable intake."
    report = tool.forward(user_info, totals, deficits, trends)

    assert "--- Nutrition Report ---" in report
    assert "Dave" in report
    assert "Protein balanced" in report
    assert "stable intake" in report
