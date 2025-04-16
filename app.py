from flask import Flask, render_template, request
from main import run, is_bengali_style, generate_bengali_recipe, analyze_ingredients, search_recipes, get_recipe_steps

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])

def index():
    if request.method == 'POST':
        user_ingredients = request.form['ingredients']
        # Step 0: Check if the query is Bengali-Style
        if is_bengali_style(user_ingredients):
            recipes = generate_bengali_recipe(user_ingredients)
            return render_template("results.html", recipe = recipes, bengali = True)
        # Step 1: If not Analyze ingredients with Gemini
        cleaned = analyze_ingredients(user_ingredients)
        ingredients = [item.replace("*", "").strip() for item in cleaned.split('\n') if item.strip() and "*" in item]
        # Step 2: Search for recipes
        recipes = search_recipes(ingredients)
        recipes_details = []

        # Step 3: Get steps for each recipe
        for recipe in recipes:
            steps = get_recipe_steps(recipe['id'])
            recipes_details.append({
                'title': recipe['title'],
                'steps': steps
            })

        return render_template('results.html', recipes=recipes_details, bengali = False, cleaned=cleaned)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

