import re

from . import RecipeHandler, SubheadingGroup, text


class TastyHandler(RecipeHandler):
    """Handler for recipes from tasty.co."""

    sites = {"tasty.co": "Tasty"}

    def title(self) -> str:
        return text(self.extract_one(".recipe-name"))

    def author(self) -> str:
        return text(self.extract_one(".byline"))

    # Unable to find a tasty.co recipe containing time information.

    def ingredients(self) -> SubheadingGroup:
        sections = self.extract(".ingredients__section")

        ingredients = {}
        for section in sections:
            name_tag = section.find(class_="ingredient-section-name")
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
        yield_text = text(self.extract_one(".servings-display"))
        return re.sub("^for ", "", yield_text)
