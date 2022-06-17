import re
from collections import defaultdict

from . import RecipeHandler, split_into_subheadings, SubheadingGroup


class SeriousEatsHandler(RecipeHandler):
    """Handler for recipes from Serious Eats.
    """
    def title(self) -> str:
        tag = self.extract_one("h1", root=".article-header")

        if tag:
            text = tag.text.strip()
            return re.sub(" Recipe$", "", text)
        return ""

    def author(self) -> str:
        tag = self.extract_one(["#mntl-byline-link_1-0", ".mntl-attribution__item-name"])

        if tag:
            text = tag.text
            text = re.sub(r"^By\s+", "", text)
            return text.strip()
        return ""

    def source(self) -> str:
        return "Serious Eats"

    def time(self) -> dict[str, str]:
        times = self.extract(".meta-text__data", root=".project-meta__times-container")
        labels = self.extract(".meta-text__label", root=".project-meta__times-container")

        times_text = [time.text.strip() for time in times]
        labels_text = [label.text.strip() for label in labels]
        labels_text = [re.sub(":$", "", label) for label in labels_text]

        return dict(zip(labels_text, times_text))

    def yield_(self) -> str:
        tag = self.extract_one(".meta-text__data", root=".project-meta__results-container")
        if tag:
            return tag.text.strip()
        return ""

    def ingredients(self) -> SubheadingGroup:
        ingredients = self.extract("ul li", root=".section--ingredients")
        ingredients_text = [ing.text.strip() for ing in ingredients]

        if any(re.match("For the ", ing, re.I) for ing in ingredients_text):
            return split_into_subheadings(ingredients_text)
        return {'': ingredients_text}

    def instructions(self) -> SubheadingGroup:
        section = self.extract_one("section#section--instructions_1-0")

        if not section:
            return {}

        for tag in section.findAll("figure"):
            tag.extract()

        instructions_tags = section.select("li")

        instructions = [re.sub(r"\n[\n\t ]+", r"\n", li.text).strip() for li in instructions_tags]
        instructions = [inst for inst in instructions if len(inst) > 0]

        if any(re.match("For the", inst, re.I) for inst in instructions):
            return split_into_subheadings(instructions)
        return {'': instructions}

    def notes(self) -> SubheadingGroup:
        tags = self.extract(["h2", "h2 + p"], root=".structured-project__steps")

        sections = defaultdict(list)

        current_section = None
        for tag in tags:
            if tag.name == 'h2':
                current_section = tag.text.strip()
            else:
                sections[current_section].append(tag.text.strip())

        return dict(sections.items())
