# Nutrition Agent

The Nutrition Agent helps you analyze your daily food intake, show you your deficits, and show you nutrition trends. 
It uses:

- **Nutritionix API** → to fetch accurate nutrient data for each food item.  
- **Google Gemini (via smolagents)** → to analyze trends and orchestrate the various tools.

---

## Prerequisites

- **Python 3.12+**  
  Make sure you are using Python 3.12 or later.

```bash
python3 --version
```

- **API Keys (stored in `.env`)**  
  You will need two sets of keys:

1. **Gemini API key**  
   - Create via [Google AI Studio](https://aistudio.google.com/) → "Get API key"  
   - Save in `.env` as:  
     ```
     GEMINI_API_KEY=your_gemini_api_key
     ```

2. **Nutritionix App ID and Key**  
   - Create via [Nutritionix Developer Portal](https://developer.nutritionix.com/)  
   - Save in `.env` as:  
     ```
     NUTRITIONIX_APP_ID=your_app_id
     NUTRITIONIX_API_KEY=your_api_key
     ```

---

## Setup

Clone the repository and move into the project:

```bash
git clone <repo-url>
cd <your-clone-location>
```

1. **Create a virtual environment**

Mac:
```bash
make .virtual_environment
source .virtual_environment/bin/activate
```

2. **Install dependencies**

On Mac:
```bash
make install-mac
```

On Linux (teacher’s original setup):
```bash
make install
```

---

## Running the Agent

Once your environment is activated and dependencies installed, run:

```bash
make agent2
```

The program will:

1. Ask if you are a returing user.
2. Ask for your **name**.
3. If returning user goto step 8, else goto step 4.
4. Ask for your **age**.
5. Ask for **weight**.
6. Ask for **height**.
7. Ask for **gender**.
8. Ask for the date for the log.
9. Prompt you to enter food items you ate today (**type 'done' when finished**).  
10. Fetch nutrition data from **Nutritionix**. 
11. Use **Gemini** to orchestrate tool usage to generate a detailed user report.

---

## Example Interaction

```text
Are you a returning user? (y/n): n
Let's set up your profile.
Enter your name: Kevin
Enter your age: 20
Enter your weight (kg): 100
Enter your height (cm): 200
Enter your gender (male/female): male
Enter the date for this log [default: 2025-09-17]: 2025-09-18

Enter each food item you ate today one at a time (type 'done' when finished):
> 2 slices of pizza
> done

Nutrition Agent Output:

--- Nutrition Report ---
User Info: Name: Kevin, Age: 20, Weight: 100.0 kg, Height: 200.0 cm, Gender: male
Daily Totals: {'calories': 569.24, 'protein': 24.38, 'carbs': 71.32, 'fat': 20.74}
Deficits/Surpluses:
{'calories': 'Deficit: 569.2 vs 2586', 'protein': 'Deficit: 24.4 vs 80', 'carbs': 'Deficit: 71.3 vs 356', 'fat': 'Deficit: 20.7 vs 86'}
Long-Term Trends:
Over the past 2 days:
- Calories averaged 569 kcal/day (range 569.24–569.24).
- Protein averaged 24.4 g/day (range 24.37–24.38).
- Carbs averaged 71.3 g/day (range 71.32–71.33).
- Fat averaged 20.7 g/day (range 20.74–20.74).

Kevin, your tracking shows a consistent intake of approximately 569 calories, 24g protein, 71g carbs, and 21g fat daily, primarily from pizza. While consistent, these numbers indicate a significant deficit across all macronutrients compared to your daily targets. Keep up the great work tracking, and consider adding more diverse foods to help meet your nutritional goals!

```

---

## Example Data

```text
{
  "name": "Kevin",
  "age": 20,
  "weight": 100.0,
  "height": 200.0,
  "gender": "male",
  "history": [
    {
      "date": "2025-09-16",
      "foods": [
        "pizza"
      ],
      "totals": {
        "calories": 569.24,
        "protein": 24.37,
        "carbs": 71.33,
        "fat": 20.74
      },
      "analysis": {
        "calories": "Deficit: 569.2 vs 2586",
        "protein": "Deficit: 24.4 vs 80",
        "carbs": "Deficit: 71.3 vs 356",
        "fat": "Deficit: 20.7 vs 86"
      }
    },
    {
      "date": "2025-09-17",
      "foods": [
        "pizza",
        "pizza"
      ],
      "totals": {
        "calories": 569.24,
        "protein": 24.38,
        "carbs": 71.32,
        "fat": 20.74
      },
      "analysis": {
        "calories": "Deficit: 569.2 vs 2586",
        "protein": "Deficit: 24.4 vs 80",
        "carbs": "Deficit: 71.3 vs 356",
        "fat": "Deficit: 20.7 vs 86"
      }
    }
  ]
}

```

---

## Testing

Minimal test fixtures are included in `tests/`.  
Run the agent tests with:

```bash
make test-agent2
```

Run the tool tests with:

```bash
make test-tools2
```