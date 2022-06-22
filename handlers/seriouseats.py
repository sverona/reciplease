import re
from collections import defaultdict

from . import RecipeHandler, split_into_subheadings, SubheadingGroup, text


class SeriousEatsHandler(RecipeHandler):
    """Handler for recipes from Serious Eats."""

    sites = {
        "seriouseats.com": "Serious Eats",
        "simplyrecipes.com": "Simply Recipes",
    }

    def title(self) -> str:
        tag = self.extract_one("h1", root=".article-header")
        return re.sub(" Recipe$", "", text(tag))

    def author(self) -> str:
        tag = self.extract_one(
            ["#mntl-byline-link_1-0", ".mntl-attribution__item-name"]
        )
        return re.sub(r"^By\s+", "", text(tag))

    def time(self) -> dict[str, str]:
        times = self.extract(
            ".meta-text__data", root=".project-meta__times-container"
        )
        labels = self.extract(
            ".meta-text__label", root=".project-meta__times-container"
        )

        times_text = [text(time) for time in times]
        labels_text = [re.sub(":$", "", text(label)) for label in labels]

        return dict(zip(labels_text, times_text))

    def yield_(self) -> str:
        tag = self.extract_one(
            ".meta-text__data", root=".project-meta__results-container"
        )
        return text(tag)

    def ingredients(self) -> SubheadingGroup:
        ingredients = self.extract("ul li", root=".section--ingredients")
        if not ingredients:
            return {}

        ingredients_text = [text(ing) for ing in ingredients]

        if any(re.match("For the ", ing, re.I) for ing in ingredients_text):
            return split_into_subheadings(ingredients_text)
        return {None: ingredients_text}

    def instructions(self) -> SubheadingGroup:
        section = self.extract_one("section#section--instructions_1-0")

        if not section:
            return {}

        for tag in section.find_all("figure"):
            tag.extract()

        instructions_tags = section.select("li")

        instructions = [
            re.sub(r"\n[\n\t ]+", r"\n", text(li)) for li in instructions_tags
        ]
        instructions = [inst for inst in instructions if len(inst) > 0]

        if any(re.match("For the", inst, re.I) for inst in instructions):
            return split_into_subheadings(instructions)
        return {None: instructions}

    def notes(self) -> SubheadingGroup:
        tags = self.extract(
            ["h2", "h2 + p"], root=".structured-project__steps"
        )

        sections = defaultdict(list)

        current_section = None
        for tag in tags:
            if tag.name == "h2":
                current_section = text(tag) or None
            else:
                sections[current_section].append(text(tag))

        return dict(sections.items())
