from re import search

from bs4 import NavigableString

from .handler import RecipeHandler


class AllrecipesHandler(RecipeHandler):
    regexes = {r"allrecipes\.com": "AllRecipes"}

    def __init__(self):
        super().__init__()

    def ingredients(self, soup: NavigableString) -> NavigableString:
        return soup.find("section", class_="recipeIngredients")

    def instructions(self, soup: NavigableString) -> NavigableString:
        return soup.find("section", class_="recipeInstructions")
