# Nutrition Agent

The Nutrition Agent helps you analyze your daily food intake.
It uses:

- **Nutritionix API** → to fetch accurate nutrient data for each food item.  
- **Google Gemini (via smolagents)** → to analyze totals, estimate calories, check for macro/micro deficits or surpluses, and suggest improvements.

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
make nutrition-agent
```

The program will:

1. Ask for your **age**.
2. Ask for your **gender**.  
3. Prompt you to enter food items you ate today (**type 'done' when finished**).  
4. Fetch nutrition data from **Nutritionix**.  
5. Use **Gemini** to analyze your day’s intake and provide feedback.  

---

## Example Interaction

```text
Enter your age: 25
Enter your gender (male or female): male

Enter each food item you ate today one at a time (type 'done' when finished):
> 1 cup of mashed potatoes and 2 tbsp gravy
> 2 slices of pizza
> 1 protein shake
> done

Nutrition Agent Output:

Estimated daily intake:
- Calories: 930.94 kcal
- Protein: 45.55 g
- Carbohydrates: 103.35 g
- Fat: 36.61 g

Then some basic analysis
```

---

## Testing

Minimal test fixtures are included in `tests/`.  
Run them with:

```bash
make pytest
```