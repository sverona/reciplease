import re

from bs4 import NavigableString

from .handler import RecipeHandler, split_into_subheads
from .extract import extract, extract_one


class WordpressHandler(RecipeHandler):
    def __init__(self):
        super(RecipeHandler, self).__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        h1 = soup.find(True, class_="wprm-recipe-name")

        return h1.text.strip()

    def author(self, soup: NavigableString) -> NavigableString:
        author_name = soup.find(True, class_="entry-author-name")

        if not author_name:
            return ""
        return author_name.text.strip()

    def yield_(self, soup: NavigableString) -> NavigableString:
        recipe_servings = soup.find(True, class_="wprm-recipe-servings")

        text = recipe_servings.text.strip()

        if re.match(r"\d+", text):
            return f"{text} servings"

        return text

    def ingredients(self, soup: NavigableString) -> NavigableString:
        div = soup.find(True, class_="wprm-recipe-ingredients-container")

        result = {}

        groups = div.find_all(True, class_="wprm-recipe-ingredient-group")

        for group in groups:
            name_container = group.find(True, class_="wprm-recipe-group-name")
            if name_container:
                name = name_container.text.strip()
                if name.endswith(":"):
                    name = name[:-1]
            else:
                name = ""

            ingredients = group.select("ul li.wprm-recipe-ingredient")
            for ingredient in ingredients:
                for checkbox in ingredient.find_all(True, class_="wprm-checkbox-container"):
                    checkbox.extract()
            ingredients = [li.text.strip() for li in ingredients]
            result[name] = ingredients

        return result

    def instructions(self, soup: NavigableString) -> NavigableString:
        div = soup.find(True, class_="wprm-recipe-instructions-container")

        result = {}

        groups = div.find_all(True, class_="wprm-recipe-instruction-group")

        for group in groups:
            name_container = group.find(True, class_="wprm-recipe-group-name")
            if name_container:
                name = name_container.text.strip()
                if name.endswith(":"):
                    name = name[:-1]
            else:
                name = ""

            instructions = group.select("ul li.wprm-recipe-instruction")
            for instruction in instructions:
                for checkbox in instruction.find_all(True, class_="wprm-checkbox-container"):
                    checkbox.extract()
            instructions = [li.text.strip() for li in instructions]
            result[name] = instructions

        return result

    def time(self, soup: NavigableString) -> NavigableString:
        section = extract_one(soup, None, [".wprm-recipe-times-container"], [], False)

        values = extract(section, None, [".wprm-recipe-time"], [])
        labels = extract(section, None, [".wprm-recipe-time-label"], [])
        labels = [re.sub(" Tim:$", "", label, re.I) for label in labels]

        accept = ["cook", "prep", "additional", "total"]
        pairs = {label.capitalize(): value for label, value in zip(labels, values) if label in accept}

        return pairs

    def notes(self, soup: NavigableString) -> NavigableString:
        div = soup.find(True, class_="wprm-recipe-notes")

        if div:
            return [div.text.strip()]

        return []
