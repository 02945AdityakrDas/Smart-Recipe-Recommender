import os
import requests
import google.generativeai as genai
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

# Set up API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Use gemini to decide if the query is Bengali-Style
def is_bengali_style(user_input):
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    prompt = f"Is the following query Bengali-Style analyze it properly? \"{user_input}\"\n"
    "Reply strictly with 'Yes' or 'No'."
    response = model.generate_content(prompt)
    return "Yes" in response.text.strip()

# generating bengali recipes


def generate_bengali_recipe(user_ingredients):
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    prompt = f"Generate a Bengali recipe with proper steps for \"{user_ingredients}\"\n, write it in Bengali."
    response = model.generate_content(prompt)
    return response.text.strip() 
# Gemini function to analyze ingredients


def analyze_ingredients(ingredients):
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    prompt = f"Given the following ingredients: {ingredients}. Clean and format them into a clear list for a recipe search."
    response = model.generate_content(prompt)
    return response.text.strip()

# Spoonacular function to search for recipes


def search_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ",".join(ingredients),
        "number": 3,
        "apiKey": SPOONACULAR_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

# Spoonacular function to get recipe steps


def get_recipe_steps(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    params = {"apiKey": SPOONACULAR_API_KEY}
    response = requests.get(url, params=params)
    steps = response.json()
    if steps and len(steps) > 0:
        return [step["step"] for step in steps[0]["steps"]]
    return ["No steps found."]


def run(user_ingredients):
    # Step 0: Check if the query is Bengali-Style
    if is_bengali_style(user_ingredients):
        print("Showing Bengali-Style recipes...")
        # Here you can add specific Bengali-Style recipe logic if needed  
        recipes =  generate_bengali_recipe(user_ingredients)
        print(recipes) 
        return
    # Step 1: Analyze ingredients with Gemini
    cleaned_ingredients = analyze_ingredients(user_ingredients)
    print("\n🧾 Cleaned Ingredients:")
    print(cleaned_ingredients)

    # Step 2: Extract individual ingredients (from Gemini's bullet format)
    ingredient_list = [
        item.replace("*", "").strip()
        for item in cleaned_ingredients.split('\n')
        if item.strip() and "*" in item
    ]

    # Step 3: Search for recipes
    recipes = search_recipes(ingredient_list)
    print("\n🍽️ Top Recipe Suggestions:")
    if not recipes:
        print("No recipes found. Try adding more or different ingredients.")
    for r in recipes:
        print(f"- {r['title']} (ID: {r['id']})")

    # Step 4: Get steps
    print("\n👨‍🍳 Cooking Steps:")
    for r in recipes:
        print(f"\nRecipe: {r['title']}")
        steps = get_recipe_steps(r['id'])
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")


# Example input
if __name__ == "__main__":
    user_ingredients = input(
        "Enter your available ingredients (comma separated): ")
    run(user_ingredients)
