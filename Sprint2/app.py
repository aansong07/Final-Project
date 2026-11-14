from flask import Flask, jsonify, render_template

app = Flask(__name__)

recipes = [
    {
        "id": 1,
        "name": "Lentil Quinoa Bowl",
        "tags": ["protein", "carbs", "fiber", "vegetarian", "vegan"],
        "prepMinutes": 30,
        "ingredients": ["lentils", "quinoa", "spinach", "cherry tomatoes", "lemon"],
        "steps": ["Cook the lentils and quinoa.", "Serve with spinach, tomatoes, and lemon."],
    },
    {
        "id": 2,
        "name": "Greek Yogurt Berry Oats",
        "tags": ["protein", "carbs", "fiber", "vegetarian"],
        "prepMinutes": 10,
        "ingredients": ["rolled oats", "Greek yogurt", "blueberries", "chia seeds"],
        "steps": ["Stir oats into Greek yogurt.", "Top with blueberries and chia seeds."],
    },
    {
        "id": 3,
        "name": "Chickpea Spinach Curry",
        "tags": ["protein", "carbs", "fiber", "vegetarian", "vegan"],
        "prepMinutes": 25,
        "ingredients": ["chickpeas", "spinach", "tomatoes", "curry powder", "brown rice"],
        "steps": ["Simmer chickpeas, tomatoes, and curry powder.", "Stir in spinach and serve with brown rice."],
    },
    {
        "id": 4,
        "name": "Salmon Sweet Potato Plate",
        "tags": ["protein", "carbs", "fiber"],
        "prepMinutes": 35,
        "ingredients": ["salmon fillet", "sweet potato", "broccoli", "olive oil"],
        "steps": ["Roast the sweet potato and broccoli.", "Bake the salmon and serve with the vegetables."],
    },
    {
        "id": 5,
        "name": "Black Bean Tacos",
        "tags": ["protein", "carbs", "fiber", "vegetarian", "vegan"],
        "prepMinutes": 20,
        "ingredients": ["black beans", "corn tortillas", "cabbage", "salsa", "avocado"],
        "steps": ["Warm the black beans and tortillas.", "Fill tortillas with beans, cabbage, salsa, and avocado."],
    },
    {
        "id": 6,
        "name": "Chicken Brown Rice Bowl",
        "tags": ["protein", "carbs"],
        "prepMinutes": 30,
        "ingredients": ["chicken breast", "brown rice", "bell pepper", "olive oil"],
        "steps": ["Cook the brown rice.", "Cook the chicken and bell pepper, then serve over rice."],
    },
    {
        "id": 7,
        "name": "Edamame Quinoa Salad",
        "tags": ["protein", "carbs", "fiber", "vegetarian", "vegan"],
        "prepMinutes": 20,
        "ingredients": ["edamame", "quinoa", "cucumber", "lemon", "parsley"],
        "steps": ["Cook the quinoa and edamame.", "Toss with cucumber, lemon, and parsley."],
    },
    {
        "id": 8,
        "name": "Cottage Cheese Veggie Toast",
        "tags": ["protein", "carbs", "fiber", "vegetarian"],
        "prepMinutes": 10,
        "ingredients": ["whole-grain bread", "cottage cheese", "tomato", "cucumber"],
        "steps": ["Toast the bread.", "Spread with cottage cheese and top with tomato and cucumber."],
    },
]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/recipes")
def get_recipes():
    return jsonify(recipes)


@app.route("/api/recipes/<recipe_id>")
def get_recipe(recipe_id):
    recipe = next((item for item in recipes if str(item["id"]) == recipe_id), None)
    if recipe is None:
        return jsonify({"error": f"Recipe with id '{recipe_id}' was not found."}), 404
    return jsonify(recipe)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
