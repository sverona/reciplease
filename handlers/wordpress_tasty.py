import re

from bs4 import Tag

from . import RecipeHandler, SubheadingGroup, text


class WordpressTastyV3Handler(RecipeHandler):
    """Handler for recipes from WordPress blogs that use Tasty Recipes V3."""

    def title(self) -> str:
        heading = self.extract_one(".tasty-recipes-title")
        return text(heading)

    def author(self) -> str:
        author_name = self.extract_one(".tasty-recipes-author-name")
        return text(author_name)

    def yield_(self) -> str:
        yield_tag = self.extract_one(
            ".tasty-recipes-yield", remove=".tasty-recipes-yield-scale"
        )
        return text(yield_tag)

    def time(self) -> dict[str, str]:
        section = self.extract_one(".tasty-recipes-details")

        if section:
            values_tags = section.find_all(
                class_=re.compile("tasty-recipes-[a-z]+-time")
            )
            values = [text(value) for value in values_tags]

            labels_tags = section.select(".tasty-recipes-label")
            labels = [
                re.sub(" Time:$", "", text(label))
                for label in labels_tags
                if re.search(" Time:$", text(label))
            ]

            acceptable_labels = ["Cook", "Prep", "Additional", "Total"]
            pairs = {
                label: value
                for label, value in zip(labels, values)
                if label in acceptable_labels
            }

            return pairs
        return {}

    def ingredients(self) -> SubheadingGroup:
        ingredients_tags = self.extract(".tasty-recipes-ingredients li")
        ingredients = [text(li) for li in ingredients_tags]
        if ingredients:
            return {None: ingredients}
        return {}

    def instructions(self) -> SubheadingGroup:
        instructions_tags = self.extract(".tasty-recipes-instructions li")
        instructions = [text(li) for li in instructions_tags]
        if instructions:
            return {None: instructions}
        return {}

    def notes(self) -> SubheadingGroup:
        notes_tags = self.extract(".tasty-recipes-notes p")
        notes = [text(p) for p in notes_tags]
        if notes:
            return {None: notes}
        return {}


class WordpressTastyPreV3Handler(WordpressTastyV3Handler):
    """Handler for recipes from WordPress blogs that use Tasty Recipes pre-V3."""

    def title(self) -> str:
        tag = self.extract_one(".tasty-recipes h2")
        return text(tag)

    def ingredients(self) -> SubheadingGroup:
        # I know of no recipe containing ingredient groups
        ingredients_tags = self.extract(".tasty-recipe-ingredients li")
        ingredients = [text(li) for li in ingredients_tags]
        if ingredients:
            return {None: ingredients}
        return {}

    def instructions(self) -> SubheadingGroup:
        instructions_tags = self.extract(".tasty-recipe-instructions li")
        instructions = [text(li) for li in instructions_tags]
        if instructions:
            return {None: instructions}
        return {}
