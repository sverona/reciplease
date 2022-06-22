import re

from flask import Flask, render_template, request, redirect
from requests.models import PreparedRequest
import requests.exceptions

from handlers import Page, Recipe
from handlers.all import ALL_HANDLERS


app = Flask(__name__)


def from_url(url: str) -> Recipe:
    """Parse a recipe from a given URL."""
    page = Page(url)

    # Try a regex match first.
    for handler in ALL_HANDLERS:
        if page.url.netloc in handler.sites:
            return Recipe(page, handler)

    for handler in ALL_HANDLERS:
        recipe = Recipe(page, handler)
        if recipe.ingredients and recipe.instructions:
            return recipe
    raise Exception("No usable handler found.")


@app.template_filter()
def wrap_fractions(text):
    return re.sub(
        r"(?:(\d+)\s+)?(\d+/\d+)", r'\1<span class="frac">\2</span>', text
    )


@app.route("/")
def index():
    return render_template("index.html")


def check_url(url):
    prepared_request = PreparedRequest()

    prepared_request.prepare_url(url, None)
    return prepared_request.url


@app.route("/reciplease", methods=["GET", "POST"])
def route_to_recipe():
    if request.method == "POST":
        url = request.form["recipeUrl"]
        try:
            check_url(url)
        except requests.exceptions.MissingSchema:
            return "404"

        return redirect(f"/{url}")
    return "404"


@app.route("/<path:url>")
def reciplease(url):
    print(url)
    try:
        check_url(url)
    except requests.exceptions.MissingSchema:
        return "404"

    recipe = from_url(url)
    return render_template("recipe.html", recipe=recipe)
