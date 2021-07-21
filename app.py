import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    """
    Route to render landing page
    """
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    """
    Route to find all recipes in the database.
    """
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Route to search functionality, using queries to search
    the database keys, for example recipe name, category,
    ingredients.
    """
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Route for the user to register to the page,
    if the username already exists flash message and the user
    is redirected to the page. The password uses werkzeug
    hashing to improve security. By insert_one the users
    profile details get added to the database.
    """
    if request.method == "POST":
        username_exist = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if username_exist:
            flash(
                "Username is already in use, please choose a different one.")

            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("You are now registred")

        return render_template("profile.html")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Search the database for username, if that exists search
    the database for password, redirects the user to profile page.
    If the username or password is incorrect the user get's a flash
    notice and then redirected to the login page.
    """
    if request.method == "POST":
        username_exist = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if username_exist:

            if check_password_hash(
                    username_exist["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for("profile", username=session["user"]))

            else:
                flash(
                    "Username or password was incorrect, please try again.")
                return redirect(url_for("login"))

        else:
            flash("The username or password was incorrect, please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    App route for the user in session to view profile page.

    Args:
    username: string - the string representation of the Mongo ID of the user.
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)


@app.route("/logout")
def logout():
    """
    End session by session.pop and redirects to home page.
    """
    session.pop("user")
    return redirect(url_for("home"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    If the user is not logged in, i.e not in session the user is
    prompted to log in to add a recipe. Returns user to login page.
    Methods: GET and POST to access and post to MongoDB
    Recipe is created by POST method, .split() to split data to
    better access it as lists in the singe_recipe page.
    """
    if 'user' not in session:
        flash("You need to be logged in to add recipes.")
        return redirect(url_for("login"))

    recipe = mongo.db.recipes.find_one_or_404(ObjectId)

    if recipe["created_by"].lower() != session['user'].lower():
        return redirect(url_for("single_recipe", recipe_id=recipe['_id']))

    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "pricing": request.form.get("pricing"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.get("ingredients").split(
                "\n", ",", "."),
            "preparation": request.form.get("preparation").split("\n"),
            "image_src": request.form.get("image_src"),
            "created_by": session["user"]
            }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added")
        return redirect(url_for("recipes"))

    categories = mongo.db.categories.find().sort(
        "category_name", 1)
    pricing = mongo.db.pricing.find().sort(
        "pricing", 1)
    cooking_time = mongo.db.cooking_time.find().sort(
        "cooking_time", 1)
    return render_template("add_recipe.html",
                           categories=categories,
                           pricing=pricing,
                           cooking_time=cooking_time)


@app.route("/single_recipe/<recipe_id>")
def single_recipe(recipe_id):
    """
    Render a single recipe page.
    Args: recipe_id (string) to access the specific recipe by id in
    MongoDB.
    """
    chosen_recipe = mongo.db.recipes.find_one_or_404({
        "_id": ObjectId(recipe_id)})
    return render_template("single_recipe.html",
                           recipe=chosen_recipe)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Takes the same string argument as single_recipe. If the
    user is not logged in they are returned to the login
    page. If the recipe is created by its user they
    are allowed to edit the recipe.
    """
    if 'user' not in session:
        flash("You need to be logged in to edit a recipe.")
        return redirect(url_for("login"))

    recipe = mongo.db.recipes.find_one_or_404(ObjectId(recipe_id))

    if recipe["created_by"].lower() != session['user'].lower():
        return redirect(url_for("single_recipe", recipe_id=recipe['_id']))

    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "pricing": request.form.get("pricing"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.get("ingredients").split(
                "\n", ",", "."),
            "preparation": request.form.get("preparation").split("\n"),
            "image_src": request.form.get("image_src"),
            "created_by": session["user"]
            }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, edit)
        flash("Recipe Successfully Edited")

    categories = mongo.db.categories.find().sort(
        "category_name", 1)
    pricing = mongo.db.pricing.find().sort(
        "pricing")
    cooking_time = mongo.db.cooking_time.find().sort(
        "cooking_time")
    return render_template("edit_recipe.html",
                           recipe=recipe,
                           categories=categories,
                           pricing=pricing,
                           cooking_time=cooking_time)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    if 'user' not in session:
        flash("You need to own this recipe to be able to delete it.")
        return redirect(url_for("login"))

    recipe = mongo.db.recipes.find_one_or_404(ObjectId(recipe_id))

    if recipe["created_by"].lower() != session['user'].lower():
        return redirect(url_for("single_recipe", recipe_id=recipe['_id']))

    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe was deleted")
    return redirect(url_for("recipes"))


@app.route("/get_categories")
def get_categories():
    """
    Finds categories and then sorts them alphabetically.
    """
    if 'user' not in session:
        flash("You need to own this recipe to be able to delete it.")
        return redirect(url_for("login"))

    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    For the user to add a category they need to be logges
    in. What gets saved to the database is the category name
    and created by. However only the creator of the database
    has access to view who added which category as this is
    not showcased in the same way as recipes.
    The new category then gets inserted to the "categories"
    object in the database.
    """
    if 'user' not in session:
        flash("You need to be logged in to create a category.")
        return redirect(url_for("login"))

    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name"),
            "created_by": session["user"]
        }
        mongo.db.categories.insert_one(category)
        flash("Category Successfully Added")
        return redirect(url_for("get_categories"))

    categories = mongo.db.categories.find().sort(
        "category_name", 1)
    return render_template("add_category.html",
                           categories=categories)


@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    Takes the argument of category_id.
    Only the admin can delete categories
    as this feature might be risky to allow
    users to use freely.
    """
    category = mongo.db.categories.find_one_or_404(ObjectId(category_id))

    if category["created_by"].lower() == "admin":
        mongo.db.categories.remove({"_id": ObjectId(category_id)})
        flash("Category was deleted")
        return redirect(url_for("get_categories"))


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    """
    Args: category_id, only admin has access to editing existing
    categories.
    """
    category = mongo.db.categories.find_one_or_404(ObjectId(category_id))

    if category["created_by"].lower() == "admin":
        if request.method == "POST":
            edit = {
                "category_name": request.form.get("category_name")}
        mongo.db.categories.update({"_id": ObjectId(category_id)}, edit)
        flash("Category was updated!")
        return redirect(url_for("get_categories"))
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


#Error Handlers

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html"), 403


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
