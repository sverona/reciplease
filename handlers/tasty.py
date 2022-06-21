import re

from . import RecipeHandler, SubheadingGroup, text


class TastyHandler(RecipeHandler):
    """Handler for recipes from tasty.co."""

    def title(self) -> str:
        title = self.soup.find(True, class_="recipe-name")
        return text(title)

    def author(self) -> str:
        byline = self.soup.find(True, class_="byline")
        return text(byline)

    def source(self) -> str:
        return "tasty.co"

    # Unable to find a tasty.co recipe containing time information.

    def ingredients(self) -> SubheadingGroup:
        sections = self.extract(".ingredients__section")

        ingredients = {}
        for section in sections:
            name_tag = section.find(True, class_="ingredient-section-name")
            if name_tag:
                name = text(name_tag)
            else:
                name = None

            ingredients_tags = section.select("ul li")
            these_ingredients = [text(li) for li in ingredients_tags]
            ingredients[name] = these_ingredients
        return ingredients

    def instructions(self) -> SubheadingGroup:
        instruction_tags = self.extract(".preparation .prep-steps li")
        if instruction_tags:
            instructions = [text(li) for li in instruction_tags]

            return {None: instructions}
        return {}

    def yield_(self) -> str:
        servings = self.soup.find(True, class_="servings-display")
        return re.sub("^for ", "", text(servings))
