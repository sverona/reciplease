from flask import Flask, render_template, request, redirect
from requests.models import PreparedRequest
import requests.exceptions

from scrape import url_to_recipe

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


def check_url(url):
    prepared_request = PreparedRequest()

    prepared_request.prepare_url(url, None)
    return prepared_request.url


@app.route('/reciplease', methods=['GET', 'POST'])
def route_to_recipe():
    if request.method == 'POST':
        url = request.form['recipeUrl']
        try:
            check_url(url)
        except requests.exceptions.MissingSchema as e:
            return '404'

        return redirect(f"/{url}")


@app.route('/<path:url>')
def reciplease(url):
    print(url)
    try:
        check_url(url)
    except requests.exceptions.MissingSchema as e:
        return '404'

    recipe = url_to_recipe(url)
    return render_template("recipe.html", recipe=recipe)
