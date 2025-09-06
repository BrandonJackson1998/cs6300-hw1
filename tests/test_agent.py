#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from agent import agent

"""
Minimal tests demonstrating agent behavior with NutritionLookup tool.
Run with: pytest -s tests/test_agent.py
"""

import pytest
from agent import agent


@pytest.mark.parametrize("age, gender, foods", [
    ("25", "male", ["1 banana"]),  # single food
    ("40", "female", ["2 slices of pizza", "1 soda"]),  # multiple foods
])
def test_agent_success(age, gender, foods):
    """Test core agent queries with different scenarios."""
    query = (
        f"Here is everything I ate and drank today as a {age} year old {gender}: "
        + "; ".join(foods)
        + ".\n"
        + "Please provide estimated calories and nutrition summary."
    )
    result = agent.run(query)
    print(f"\n--- Agent Result ({foods}) ---\n{result}\n")
    assert isinstance(result, str)
    assert "protein" in result.lower()
    assert "carb" in result.lower()
    assert "fat" in result.lower()

@pytest.mark.parametrize("age, gender, foods", [
    ("30", "male", ["dragonfire elixir"]), # fictional food
    ("30", "male", ["battery acid"]), # not food
])
def test_agent_unrecognized_food(age, gender, foods):
    """Agent should handle unrecognized food items gracefully."""
    query = (
        f"Here is everything I ate and drank today as a {age} year old {gender}: "
        + "; ".join(foods)
        + ".\n"
        + "Please provide estimated calories and nutrition summary."
    )
    result = agent.run(query)
    print(f"\n--- Agent Result ({foods}) ---\n{result}\n")
    assert isinstance(result, str)
    assert "protein" not in result.lower()
    assert "carb" not in result.lower()
    assert "fat" not in result.lower()

def test_agent_empty_food_list():
    """Agent should handle empty food gracefully (though agent.py normally prevents this)."""
    query = (
        "Here is everything I ate and drank today as a 25 year old male: .\n"
        "Please provide estimated calories."
    )
    result = agent.run(query)
    print("\n--- Agent Result (empty foods) ---\n", result)
    assert "protein" not in result.lower()
    assert "carb" not in result.lower()
    assert "fat" not in result.lower()
