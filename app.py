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
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username_exist = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if username_exist:
            flash("This username is already in use, please choose a different one.")

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
    if request.method == "POST":
        username_exist = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if username_exist:
            if check_password_hash(
                username_exist["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    return redirect(url_for(
                        "profile", username=session["user"]))

            else:
                flash(
                    "The username or password was incorrect, please try again.")
                return redirect(url_for("login"))

        else:
            flash("The username or password was incorrect, please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    return render_template("profile.html", username=username)


@app.route("/logout")
def logout():
    if session.pop("user"):
        return render_template("index.html")


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "pricing": request.form.get("pricing"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.getlist("ingredients"),
            "preparation": request.form.get("preparation"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added")
        return redirect(url_for("recipes"))

    categories = mongo.db.categories.find().sort(
        "category_name", 1)
    pricing = mongo.db.recipes.find().sort(
        "pricing", 1)
    cooking_time = mongo.db.recipes.find().sort(
        "cooking_time", 1)
    return render_template("add_recipe.html",
                           categories=categories,
                           pricing=pricing,
                           cooking_time=cooking_time)


@app.route("/single_recipe/<recipe_id>")
def single_recipe(recipe_id):
    chosen_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("single_recipe.html",
                           recipe=chosen_recipe)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name"),
            "recipe_name": request.form.get("recipe_name"),
            "pricing": request.form.get("pricing"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.getlist("ingredients"),
            "preparation": request.form.get("preparation"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, edit)
        flash("Recipe Successfully Edited")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    categories = mongo.db.categories.find().sort(
        "category_name", 1)
    pricing = mongo.db.recipes.find().sort(
        "pricing", 1)
    cooking_time = mongo.db.recipes.find().sort(
        "cooking_time", 1)
    return render_template("edit_recipe.html",
                           recipe=recipe,
                           categories=categories,
                           pricing=pricing,
                           cooking_time=cooking_time)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe was deleted")
    return redirect(url_for("recipes"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
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
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Categort was deleted")
    return redirect(url_for("get_categories"))


@app.route("/edit_category/<category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        edit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)},edit)
        flash("Category was updated!")
        return redirect(url_for("get_categories"))
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=os.environ.get("PORT"),
            debug=True)
