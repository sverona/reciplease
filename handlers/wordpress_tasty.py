import re

from bs4 import NavigableString

from .handler import RecipeHandler, split_into_subheads


class WordpressTastyHandler(RecipeHandler):
    regexes = {
        r"sallysbakingaddiction\.com": "Sally's Baking Addiction",
        r"thymetochange\.com": "Thyme To Change",
    }

    def __init__(self):
        super(RecipeHandler, self).__init__()

    def title(self, soup: NavigableString) -> NavigableString:
        h1 = soup.find(True, class_="tasty-recipes-title")

        return h1.text.strip()

    def author(self, soup: NavigableString) -> NavigableString:
        author_name = soup.find(True, class_="tasty-recipes-author-name")

        if author_name:
            return author_name.text.strip()
        return ""

    def yield_(self, soup: NavigableString) -> NavigableString:
        recipe_servings = soup.find(True, class_="tasty-recipes-yield")

        for tag in recipe_servings.find_all(True, class_="tasty-recipes-yield-scale"):
            tag.extract()

        text = recipe_servings.text.strip()

        if re.fullmatch(r"\d+", text):
            return f"{text} servings"

        return text

    def ingredients(self, soup: NavigableString) -> NavigableString:
        div = soup.find(True, class_="tasty-recipes-ingredients")

        result = {}

        def is_actual_ingredients_container(tag):
            return any(t.name in ["ol", "ul"] for t in tag.children)

        ingredients_container = div.find(is_actual_ingredients_container, class_="tasty-recipes-ingredients-body")

        name = ""
        for tag in ingredients_container.children:
            if tag.name == "ul" or tag.name == "ol":
                ingredients = tag.find_all("li")
                ingredients = [li.text.strip() for li in ingredients]

                result[name] = ingredients
                name = ""
            elif not isinstance(tag, NavigableString):
                name = tag.text.strip()

        return result

    def instructions(self, soup: NavigableString) -> NavigableString:
        instructions = soup.find(True, class_="tasty-recipes-instructions-body")
        instructions = [li.text.strip() for li in instructions.find_all("li")]

        return split_into_subheads(instructions)

    def total_time(self, soup: NavigableString) -> NavigableString:
        recipe_time = soup.find(True, class_="tasty-recipes-total-time")

        return recipe_time.text.strip()

    def active_time(self, soup: NavigableString) -> NavigableString:
        recipe_time = soup.find(True, class_="tasty-recipes-prep-time")

        return recipe_time.text.strip()

    def notes(self, soup: NavigableString) -> NavigableString:
        div = soup.find(True, class_="tasty-recipes-notes")

        print(div)

        if div:
            print(div.find_all("p"))
            return [p.text.strip() for p in div.find_all(["p", "li"])]

        return []
