import re
from collections import defaultdict

from bs4 import NavigableString

from .extract import extract, extract_one
from .handler import RecipeHandler, split_into_subheads


class SeriousEatsHandler(RecipeHandler):
    regexes = {r"seriouseats\.com": "Serious Eats"}

    def __init__(self):
        super().__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        text = extract_one(soup, ".article-header", ["h1"], [])
        return re.sub(" Recipe$", "", text)

    def author(self, soup: NavigableString) -> NavigableString:
        text = extract_one(soup, None, ["#mntl-byline-link_1-0", ".mntl-attribution__item-name"], [])

        if text:
            text = re.sub(r"^By\s+", "", text)
            return text.strip()
        return "Serious Eats"

    def time(self, soup: NavigableString) -> NavigableString:
        times = extract(soup, ".project-meta__times-container", [".meta-text__data"], [])
        labels = extract(soup, ".project-meta__times-container", [".meta-text__label"], [])

        labels = [re.sub(":$", "", label) for label in labels]

        return {label: time for label, time in zip(labels, times)}

    def yield_(self, soup: NavigableString) -> NavigableString:
        yield_ = extract_one(soup, ".project-meta__results-container", [".meta-text__data"], [])
        return yield_

    def ingredients(self, soup: NavigableString) -> NavigableString:
        ingredients = extract(soup, ".section--ingredients", ["ul li"], [])

        if any(re.match("For the ", ing, re.I) for ing in ingredients):
            return split_into_subheads(ingredients)
        else:
            return {'': ingredients}

    def instructions(self, soup: NavigableString) -> NavigableString:
        section = soup.find("section", id="section--instructions_1-0")

        for tag in section.findAll("figure"):
            tag.extract()

        instructions = section.select("ol li")
        if not instructions:
            instructions = section.select("ul li")

        instructions = [re.sub(r"\n[\n\t ]+", r"\n", li.text).strip() for li in instructions]

        instructions = [inst for inst in instructions if len(inst) > 0]

        if any(re.match("For the", inst, re.I) for inst in instructions):
            return split_into_subheads(instructions)
        else:
            return {'': instructions}

    def notes(self, soup: NavigableString) -> NavigableString:
        tags = extract(soup, ".structured-project__steps", ["h2", "h2 + p"], [], as_text=False)

        sections = defaultdict(list)

        current_section = ''
        for tag in tags:
            if tag.name == 'h2':
                current_section = tag.text.strip()
            else:
                sections[current_section].append(tag.text.strip())

        return sections
