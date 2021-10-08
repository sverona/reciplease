import re

from bs4 import NavigableString

from .handler import RecipeHandler
from .extract import extract, extract_one


class AllrecipesHandler(RecipeHandler):
    regexes = {r"allrecipes\.com": "AllRecipes"}

    def __init__(self):
        super().__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        return extract_one(soup, ".recipe-main-header", ["h1"], [])

    def ingredients(self, soup: NavigableString) -> NavigableString:
        sections = extract(soup, None, [".ingredients-section__fieldset"], [], False)

        headings = [extract_one(section, None, [".ingredients-section__legend"], []) for section in sections]

        headings = [re.sub("^For the ", "", heading, re.I) for heading in headings]
        headings = [re.sub(":$", "", heading, re.I) for heading in headings]

        ingredients = {heading: extract(section, None, ["li"], []) for heading, section in zip(headings, sections)}

        return ingredients

    def instructions(self, soup: NavigableString) -> NavigableString:
        sections = extract(soup, None, [".instructions-section"], [], False)

        steps = [extract(section, None, [".section-body"], []) for section in sections]

        return {'': steps[0]}

    def yield_(self, soup: NavigableString) -> NavigableString:
        section = extract_one(soup, ".recipe-content-container", [".recipe-info-section"], [], False)

        values = extract(section, None, [".recipe-meta-item-body"], [])
        labels = extract(section, None, [".recipe-meta-item-header"], [])
        labels = [re.sub(":$", "", label, re.I) for label in labels]

        pairs = {label.capitalize(): value for label, value in zip(labels, values)}

        if "Yield" in pairs.keys():
            return pairs["Yield"]
        if "Servings" in pairs.keys():
            return pairs["Servings"]
        return ""

    def time(self, soup: NavigableString) -> NavigableString:
        section = extract_one(soup, ".recipe-content-container", [".recipe-info-section"], [], False)

        values = extract(section, None, [".recipe-meta-item-body"], [])
        labels = extract(section, None, [".recipe-meta-item-header"], [])
        labels = [re.sub(":$", "", label, re.I) for label in labels]

        accept = ["cook", "prep", "additional", "total"]
        pairs = {label.capitalize(): value for label, value in zip(labels, values) if label in accept}

        return pairs

    def notes(self, soup: NavigableString) -> NavigableString:
        sections = extract(soup, ".recipe-notes", [".recipe-note"], [], False)

        headings = [extract_one(section, None, ["h2"], []) for section in sections]
        headings = [re.sub(":$", "", heading, re.I) for heading in headings]
        notes = [extract(section, None, [".paragraph"], []) for section in sections]

        return {heading: note for heading, note in zip(headings, notes)}

    def author(self, soup: NavigableString) -> NavigableString:
        return extract_one(soup, ".author", [".author-name"], [])
