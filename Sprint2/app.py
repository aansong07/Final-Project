from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

ALLOWED_TAGS = {"protein", "carbs", "fiber", "vegetarian", "vegan"}

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


def clean_recipe_data(data):
    if not isinstance(data, dict):
        return None, "Request body must be a JSON object."

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        return None, "'name' must be a non-empty string."

    prep_minutes = data.get("prepMinutes")
    if isinstance(prep_minutes, bool):
        return None, "'prepMinutes' must be a positive integer."
    if isinstance(prep_minutes, str):
        prep_minutes = prep_minutes.strip()
        try:
            prep_minutes = int(prep_minutes)
        except ValueError:
            return None, "'prepMinutes' must be a positive integer."
    elif not isinstance(prep_minutes, int):
        return None, "'prepMinutes' must be a positive integer."
    if prep_minutes <= 0:
        return None, "'prepMinutes' must be a positive integer."

    tags = data.get("tags")
    if not isinstance(tags, list):
        return None, "'tags' must be a list of allowed tag strings."
    cleaned_tags = []
    for tag in tags:
        if not isinstance(tag, str):
            return None, "'tags' must contain only allowed tag strings."
        tag = tag.strip()
        if tag not in ALLOWED_TAGS:
            return None, f"'{tag}' is not an allowed tag."
        if tag not in cleaned_tags:
            cleaned_tags.append(tag)

    cleaned_recipe = {
        "name": name.strip(),
        "tags": cleaned_tags,
        "prepMinutes": prep_minutes,
    }
    for field in ("ingredients", "steps"):
        values = data.get(field)
        if not isinstance(values, list):
            return None, f"'{field}' must be a list of strings."
        if any(not isinstance(value, str) or not value.strip() for value in values):
            return None, f"'{field}' must contain non-empty strings."
        cleaned_recipe[field] = [value.strip() for value in values]

    return cleaned_recipe, None


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


@app.route("/api/recipes", methods=["POST"])
def create_recipe():
    recipe_data, error = clean_recipe_data(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    recipe = {
        "id": max((item["id"] for item in recipes), default=0) + 1,
        **recipe_data,
    }
    recipes.append(recipe)
    return jsonify(recipe), 201


@app.route("/api/recipes/<recipe_id>", methods=["PUT"])
def update_recipe(recipe_id):
    recipe = next((item for item in recipes if str(item["id"]) == recipe_id), None)
    if recipe is None:
        return jsonify({"error": f"Recipe with id '{recipe_id}' was not found."}), 404

    recipe_data, error = clean_recipe_data(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    recipe.update(recipe_data)
    return jsonify(recipe)


@app.route("/api/recipes/<recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = next((item for item in recipes if str(item["id"]) == recipe_id), None)
    if recipe is None:
        return jsonify({"error": f"Recipe with id '{recipe_id}' was not found."}), 404
    recipes.remove(recipe)
    return "", 204


@app.errorhandler(404)
def handle_not_found(_error):
    return jsonify({"error": "Not found."}), 404


@app.errorhandler(500)
def handle_internal_error(_error):
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
