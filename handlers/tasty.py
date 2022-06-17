from . import RecipeHandler, SubheadingGroup

class TastyHandler(RecipeHandler):
    """Handler for recipes from tasty.co.
    """
    def title(self) -> str:
        title = self.soup.find(True, class_="recipe-name")
        if title:
            return title.text.strip()
        return ""

    def author(self) -> str:
        byline = self.soup.find(True, class_="byline")
        if byline:
            return byline.text.strip()
        return ""

    def source(self) -> str:
        return "tasty.co"

    def time(self) -> dict[str, str]:
        return {}

    def ingredients(self) -> SubheadingGroup:
        sections = self.extract(".ingredients__section")

        ingredients = {}
        for section in sections:
            name_tag = section.find(True, class_="ingredient-section-name")
            if name_tag:
                name = name_tag.text.strip()
            else:
                name = None

            ingredients_tags = section.select("ul li")
            these_ingredients = [li.text.strip() for li in ingredients_tags]
            print(name, these_ingredients)
            ingredients[name] = these_ingredients
        return ingredients

    def instructions(self) -> SubheadingGroup:
        instruction_tags = self.extract(".preparation .prep-steps li")
        if instruction_tags:
            instructions = [li.text.strip() for li in instruction_tags]

            return {None: instructions}
        return {}

    def yield_(self) -> str:
        servings = self.soup.find(True, class_="servings-display")
        if servings:
            if servings.text.startswith("for "):
                return servings.text[4:]
            return servings.text
        return ""
