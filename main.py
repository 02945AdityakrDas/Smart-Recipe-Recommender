import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')
# Function to generate a recipe based on ingredients and cuisine type
def generate_recipe(ingredients, cuisine_type):
    if cuisine_type.lower() == "bengali":
        prompt = f"""
        Generate a Bengali recipe using these ingredients: {ingredients}.
        The recipe should include the dish name, a short intro, ingredients list, and step-by-step instructions.
        Write the entire recipe in Bengali.
        """
    else:
        prompt = f"""
        Generate a {cuisine_type} style recipe using these ingredients: {ingredients}.
        The recipe should include the dish name, a short intro, ingredients list, and step-by-step instructions.
        Write the recipe in English.
        """

    response = model.generate_content(prompt)
    return response.text.strip()

def run():
    ingredients = input("Enter available ingredients (comma separated): ")
    cuisine_type = input(
        "Enter desired cuisine (e.g., Bengali, English, Chinese, Italian, etc.): ")

    print(f"\n🍽️ Generating a {cuisine_type} recipe using: {ingredients}...\n")
    recipe = generate_recipe(ingredients, cuisine_type)
    print(recipe)

if __name__ == "__main__":
    run()
