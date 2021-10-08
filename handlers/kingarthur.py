import re

from bs4 import NavigableString

from .handler import RecipeHandler, split_into_subheads
from .extract import extract, extract_one


class KingArthurHandler(RecipeHandler):
    regexes = {r"kingarthurbaking\.com": "King Arthur Baking"}

    def __init__(self):
        super().__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        header = soup.find("section", class_="page-content-header")

        h1 = header.find("h1")

        return h1.text.strip()

    def author(self, soup: NavigableString) -> NavigableString:
        author = extract_one(soup, ".article__author", [], [])
        if author:
            return re.sub(r"^By\s+", "", author).strip()
        return "King Arthur Baking"

    def ingredients(self, soup: NavigableString) -> NavigableString:
        ingredients = {}
        subheads = extract(soup, ".ingredients-list", [".ingredient-section"], [], False)
        for subhead in subheads:
            if subhead.find("p"):
                title = subhead.find("p").text
            else:
                title = ''
            ingredients[title] = [li.text.strip() for li in subhead("li")]
        return ingredients

    def instructions(self, soup: NavigableString) -> NavigableString:
        instructions = extract(soup, ".field--recipe-steps", ["ol li", "ul li"], ["li aside", ".share"])

        return split_into_subheads(instructions)

    def yield_(self, soup: NavigableString) -> NavigableString:
        box = soup.find(True, class_="stat__item--yield")

        span = box.find("span")

        return span.text.strip()

    def time(self, soup: NavigableString) -> NavigableString:
        times = extract(soup, ".stats--recipe", [".stat__item span"], [])
        labels = extract(soup, ".stats--recipe", [".stat__item .label"], [])

        return {label: time for label, time in zip(labels, times)}

    def notes(self, soup: NavigableString) -> NavigableString:
        notes = extract(soup, None, [".recipe__tips ul li", ".ingredient-section__footnote"], [])

        return notes
