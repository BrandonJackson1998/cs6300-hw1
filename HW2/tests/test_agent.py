#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from unittest.mock import patch
from datetime import date
from agent import agent


# ---------------------------
# Tests
# ---------------------------
@pytest.mark.parametrize("user, foods", [
    (["Sam", 25, 80.0, 175.0, "male"], ["banana"]),
])
def test_agent_success(user, foods):
    """Test agent with recognized foods."""

    name, age, weight, height, gender = user
    today = str(date.today())

    query = (
        f"User: {name}, {age} years old {gender}, {weight}kg, {height}cm. "
        f"Date: {today}. "
        f"Food eaten: {', '.join(foods)}.\n"
        "Create the user and estimate calories, check for macro/micro deficits or surpluses, "
        "and provide suggestions."
    )

    result = agent.run(query)
    assert isinstance(result, str)
    assert "User Info: Name: Sam, Age: 25, Weight: 80.0 kg, Height: 175.0 cm, Gender: male" in result
    assert "Daily Totals:" in result
    assert "Deficits/Surpluses:" in result
    assert "Long-Term Trends:" in result