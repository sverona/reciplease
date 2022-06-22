import re

from . import RecipeHandler, SubheadingGroup, text


class Food52Handler(RecipeHandler):
    """Handler for recipes from food52.com."""

    sites = {"food52.com": "Food52"}

    def title(self) -> str:
        return text(self.extract_one(".recipe__title"))

    def author(self) -> str:
        author_text = text(self.extract_one(".meta__author"), squeeze=True)
        author_text = re.sub("^by: ", "", author_text)
        author_text = author_text.title()

        return author_text

    def yield_(self) -> str:
        details = self.extract_one(".recipe__details")

        if not details:
            return ""

        yield_container = details.find(lambda tag: "Serves" in tag.text)
        return text(yield_container, squeeze=True)

    def ingredients(self) -> SubheadingGroup:
        ingredients: SubheadingGroup = {}

        sections = self.extract(".recipe__list--ingredients ul")
        for section in sections:
            title_tag = section.find("li", class_="recipe__list-subheading")
            if title_tag:
                title = text(title_tag)
                title = re.sub("^For the ", "", title)
                title = re.sub(":$", "", title)
                title = title.capitalize()
            else:
                title = None
            these_tags = section.find_all("li", class_=None)
            these_ingredients = [text(tag, squeeze=True) for tag in these_tags]

            ingredients[title] = these_ingredients

        return ingredients

    def instructions(self) -> SubheadingGroup:
        instructions: SubheadingGroup = {}

        sections = self.extract(".recipe__list--steps ol")
        for section in sections:
            title_tag = section.find("li", class_="recipe__list-subheading")
            if title_tag:
                title = text(title_tag)
                title = re.sub("^For the ", "", title)
                title = re.sub(":$", "", title)
                title = title.capitalize()
            else:
                title = None
            these_tags = section.find_all("li", class_="recipe__list-step")
            these_instructions = [text(tag) for tag in these_tags]

            instructions[title] = these_instructions

        return instructions
