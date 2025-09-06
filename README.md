# Nutrition Agent

The Nutrition Agent helps you analyze your daily food intake.
It uses:

Nutritionix API
 → to fetch accurate nutrient data for each food item.

Google Gemini (via smolagents)
 → to analyze totals, estimate calories, check for macro/micro deficits or surpluses, and suggest improvements.

## Prerequisites

Python 3.12+
Make sure you are using Python 3.12 or later.

python3 --version


API Keys (stored in .env)
You will need two sets of keys:

Gemini API key

Create via Google AI Studio
 → "Get API key"

Save in .env as:

GEMINI_API_KEY=your_gemini_api_key


Nutritionix App ID and Key

Create via Nutritionix Developer Portal

Save in .env as:

NUTRITIONIX_APP_ID=your_app_id
NUTRITIONIX_API_KEY=your_api_key

## Setup

Clone the repository and move into the project:

git clone <your-repo-url>
cd <your-project-name>

1. Create a virtual environment
macOS / Linux
python3 -m venv .virtual_environment
source .virtual_environment/bin/activate

Windows (PowerShell)
python -m venv .virtual_environment
.\.virtual_environment\Scripts\activate

2. Install dependencies

On macOS:

make install-mac


On Linux (teacher’s original setup):

make install


Or install directly with pip:

pip install -r requirements.txt

## Running the Agent

Once your environment is activated and dependencies installed, run:

make nutrition-agent


or directly:

python src/agent.py


The program will:

Ask for your age and gender.

Prompt you to enter food items you ate today (done when finished).

Fetch nutrition data from Nutritionix.

Use Gemini to analyze your day’s intake and provide feedback.

## Example Interaction
Enter your age: 25
Enter your gender (male or female): male

Enter each food item you ate today one at a time (type 'done' when finished):
> 1 cup of mashed potatoes and 2 tbsp gravy
> 2 slices of pizza
> 1 protein shake
> done

Nutrition Agent Output:
- Total calories: ~2,450 kcal
- Protein intake: adequate
- Carbohydrates: slightly high
- Fat: balanced
- Consider adding vegetables for more fiber and micronutrients

## Testing

Minimal test fixtures are included in tests/.
Run them with:

pytest -s


Make sure your PYTHONPATH includes src/:

PYTHONPATH=src pytest -s tests/

