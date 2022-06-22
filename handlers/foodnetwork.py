import re

from . import RecipeHandler, split_into_subheadings, SubheadingGroup, text


class FoodNetworkHandler(RecipeHandler):
    """Handler for recipes from foodnetwork.com."""

    sites = {"foodnetwork.com": "Food Network"}

    def title(self) -> str:
        return text(self.extract_one(".o-AssetTitle"))

    def author(self) -> str:
        author_tag = self.extract_one(".o-Attribution__m-Author")
        author_text = text(author_tag, squeeze=True)
        author_text = re.sub("^Recipe courtesy of ", "", author_text)

        return author_text

    def yield_(self) -> str:
        yield_tag = self.extract_one(
            ".o-RecipeInfo__m-Yield .o-RecipeInfo__a-Description"
        )

        return text(yield_tag)

    def time(self) -> dict[str, str]:
        times = {}

        time_tags = self.extract(".o-RecipeInfo__m-Time li")
        for container in time_tags:
            title_tag = container.find(class_="o-RecipeInfo__a-Headline")
            value_tag = container.find(class_="o-RecipeInfo__a-Description")

            if not (title_tag and value_tag):
                continue

            title_text = re.sub(":$", "", text(title_tag))
            value_text = text(value_tag)

            times[title_text] = value_text

        return times

    def ingredients(self) -> SubheadingGroup:
        container = self.extract_one(".o-Ingredients__m-Body")

        if not container:
            return {}

        for remove in container.find_all(
            class_="o-Ingredients__a-Ingredient--SelectAll"
        ):
            remove.extract()

        tags = container.select(
            ".o-Ingredients__a-SubHeadline, .o-Ingredients__a-Ingredient"
        )
        texts = [text(tag) for tag in tags]
        groups = split_into_subheadings(texts)

        instructions = {}
        for title, group in groups.items():
            if title:
                title = re.sub("^For the ", "", title)
                title = re.sub(":$", "", title)
            instructions[title] = group

        return instructions

    def instructions(self) -> SubheadingGroup:
        steps = self.extract(".o-Method__m-Body .o-Method__m-Step")

        if not steps:
            return {}
        return {None: [text(step) for step in steps]}
