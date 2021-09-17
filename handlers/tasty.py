import re

from bs4 import NavigableString

from .handler import RecipeHandler, split_into_subheads


class TastyHandler(RecipeHandler):
    regexes = {r"tasty\.co": "Tasty"}

    def __init__(self):
        super().__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        title = soup.find(True, class_="recipe-name")

        return title.text.strip()

    def author(self, soup: NavigableString) -> NavigableString:
        byline = soup.find(True, class_="byline")

        if not byline:
            return "Tasty"
        return byline.text.strip()

    def active_time(self, soup: NavigableString) -> NavigableString:
        prep_time = soup.find(lambda tag: "Prep Time" in tag.text, class_="recipe-time")

        actual_time = prep_time.find(True, class_="md-block")
        return actual_time.text.strip()

    def total_time(self, soup: NavigableString) -> NavigableString:
        total_time = soup.find(lambda tag: "Total Time" in tag.text, class_="recipe-time")

        actual_time = total_time.find(True, class_="md-block")
        return actual_time.text.strip()

    def ingredients(self, soup: NavigableString) -> NavigableString:
        section = soup.find(True, class_="ingredients-prep")

        groups = section.find(True, class_="ingredients__section")

        ingredients = section.select("ul li")
        ingredients = [li.text.strip() for li in ingredients]

        return {'': ingredients}

    def instructions(self, soup: NavigableString) -> NavigableString:
        section = soup.find(True, class_="preparation")

        groups = section.find(True, class_="prep-steps")

        instructions = groups.select("li")
        instructions = [li.text.strip() for li in instructions]

        return {'': instructions}

    def yield_(self, soup: NavigableString) -> NavigableString:
        servings = soup.find(True, class_="servings-display")
        if servings.text.startswith("for "):
            return servings.text[4:]
        return servings.text
