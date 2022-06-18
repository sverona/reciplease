import re

from . import RecipeHandler, SubheadingGroup, text


class DelishHandler(RecipeHandler):
    """Handler for recipes from delish.com.
    """

    def title(self) -> str:
        tag = self.extract_one(".recipe-hed")
        return text(tag)

    def author(self) -> str:
        tag = self.extract_one(".byline-name")
        return text(tag)

    def source(self) -> str:
        return "Delish"

    def yield_(self) -> str:
        tag = self.extract_one(".yields-amount")
        return text(tag, squeeze=True)

    def time(self) -> dict[str, str]:
        tags = self.soup.find_all("span",
                                  class_=re.compile("[a-z]+-time-amount"))

        times = {}
        for tag in tags:
            match = re.match("[a-z]+", tag["class"][0])
            if match:
                key = match.group(0).capitalize()
                times[key] = text(tag, squeeze=True)

        return times

    def ingredients(self) -> SubheadingGroup:
        sections = self.extract(".ingredient-section")

        ingredients = {}
        for section in sections:
            header = section.find(class_="ingredient-title")
            header_name = text(header, squeeze=True) or None

            these_ingredients = section.find_all(class_="ingredient-item")
            ingredients[header_name] = [text(ing, squeeze=True)
                                        for ing in these_ingredients]
        return ingredients

    def instructions(self) -> SubheadingGroup:
        sections = self.extract(".direction-section")

        instructions = {}
        for section in sections:
            header = section.find(class_="direction-title")
            header_name = text(header, squeeze=True) or None

            these_instructions = section.find_all(["li", "p"])
            instructions[header_name] = [text(ins, squeeze=True)
                                         for ins in these_instructions]
        return instructions

    # I was unable to find a Delish recipe with a notes section.
