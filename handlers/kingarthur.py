import re

from bs4 import NavigableString

from .handler import RecipeHandler, split_into_subheads
from .extract import extract


class KingArthurHandler(RecipeHandler):
    regexes = {r"kingarthurbaking\.com": "King Arthur Baking"}

    def __init__(self):
        super().__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        header = soup.find("section", class_="page-content-header")

        h1 = header.find("h1")

        return h1.text.strip()

    def author(self, soup: NavigableString) -> NavigableString:
        article_author = soup.find("p", class_="article__author")

        if article_author is not None:
            text = article_author.text
            return re.sub(r"^By\s+", "", text).strip()
        else:
            return "King Arthur Baking"

    def ingredients(self, soup: NavigableString) -> NavigableString:
        section = soup.find(True, class_="ingredients-list")

        ingredients = {}
        for subhead in section.findAll("div", class_="ingredient-section"):
            if subhead.find("p"):
                title = subhead.find("p").text
            else:
                title = ''
            ingredients[title] = [li.text.strip() for li in subhead("li")]
        return ingredients

    def instructions(self, soup: NavigableString) -> NavigableString:
        section = soup.find(True, class_="field--recipe-steps")

        for tag in section.select("li aside"):
            tag.extract()

        instructions = section.select("ol li")
        if not instructions:
            instructions = section.select("ul li")

        instructions = [re.sub(r"\n[\n\t ]+", r"\n", li.text).strip() for li in instructions]

        instructions = [inst for inst in instructions if len(inst) > 0]

        print(instructions)

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
