from flask import Flask, render_template, request
from main import generate_recipe

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ingredients = request.form['ingredients']
        cuisine_type = request.form['cuisine_type']

        # Generate the recipe using Gemini
        recipe = generate_recipe(ingredients, cuisine_type)

        is_bengali = cuisine_type.strip().lower() == "bengali"

        return render_template(
            "results.html",
            recipe=recipe,
            bengali=is_bengali,
            ingredients=ingredients,
            cuisine=cuisine_type
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
