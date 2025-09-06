
- Need Gemini API key. Store in `.env/GEMINI_API_KEY`
- Need Nutritionix APP ID. Store in `.env/NUTRITIONIX_APP_ID`
- Need Nutritionix API key. Store in `.env/NUTRITIONIX_API_KEY`

- [Create Gemini API Key](https://aistudio.google.com/) "Get API key"
- [Create Nutritionix ID and Key] (https://developer.nutritionix.com/)


# Nutrition Agent

This project uses [smolagents](https://github.com/huggingface/smolagents) with Google Gemini to analyze your daily food intake.  
It uses Nutritionix to obtain nutrient data for each food item.
The agent will then estimates your calories, checks for potential macro/micro nutrient deficits, and can suggest improvements.

## Requirements

1. **Setup**:
For my Mac this is my setup steps

make .virtual_environment
source .virtual_environment/bin/activate
make install-mac     
make nutrition-agent or python src/agent.py

For teacher on Linux these were what was here originally, but these didn't work for me.

make .virtual_environment
make install 
make nutrition-agent or python src/agent.py
