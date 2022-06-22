import re

from . import RecipeHandler, SubheadingGroup, text


class BBCHandler(RecipeHandler):
    """Handler for recipes from bbcgoodfood.com."""

    sites = {"bbcgoodfood.com": "BBC Good Food"}

    def title(self) -> str:
        tag = self.extract_one(".heading-1", root=".headline")
        return text(tag)

    def author(self) -> str:
        tag = self.extract_one(".author-link")
        tag_text = text(tag)
        return re.sub("^By ", "", tag_text)

    def yield_(self) -> str:
        tag = self.extract_one(".post-header__servings")
        tag_text = text(tag)
        return re.sub("^Serves ", "", tag_text)

    def ingredients(self) -> SubheadingGroup:
        section = self.extract_one(".recipe__ingredients")
        ingredients = {}
        if section:
            for subsection in section.find_all("section"):
                heading = subsection.find("h3")
                if heading:
                    title = heading.text
                else:
                    title = None

                ingredients_tags = subsection.find_all("li")
                ingredients[title] = [text(ing) for ing in ingredients_tags]
        return ingredients

    def instructions(self) -> SubheadingGroup:
        # Don't know of a BBC recipe with instruction sections yet.

        section = self.extract_one(".recipe__method-steps")
        if section:
            for heading in section.find_all(class_="heading-6"):
                heading.extract()

            instructions_tags = section.find_all("li")
            instructions = [text(ins) for ins in instructions_tags]
            return {None: instructions}
        return {}

    def time(self) -> dict[str, str]:
        tags = self.extract(".cook-and-prep-time li")

        times = [text(tag) for tag in tags]
        # FIXME This is bad, go by tags instead.
        return {t.split(":")[0]: t.split(":")[1] for t in times if ":" in t}
