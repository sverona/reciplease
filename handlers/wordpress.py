import re

from bs4 import Tag

from . import RecipeHandler, SubheadingGroup, text


class WordpressHandler(RecipeHandler):
    """Handler for recipes from blogs that use Wordpress Recipe Manager (WPRM)."""

    def title(self) -> str:
        title = self.extract_one(
            ".wprm-recipe-name", remove=".wprm-recipe-roundup-item"
        )
        return text(title)

    def author(self) -> str:
        author_name = self.extract_one(
            ".entry-author-name", remove=".wprm-recipe-roundup-item"
        )
        return text(author_name)

    def source(self) -> str:
        site_name = self.soup.find("meta", attrs={"property": "og:site_name"})

        if isinstance(site_name, Tag):
            content = site_name.attrs["content"]
            if isinstance(content, str):
                return content
            return ", ".join(content)
        return ""

    def yield_(self) -> str:
        recipe_servings = self.soup.find(True, class_="wprm-recipe-servings")

        servings_text = text(recipe_servings)

        if re.match(r"\d+", servings_text):
            return f"{servings_text} servings"
        return servings_text

    def ingredients(self) -> SubheadingGroup:
        div = self.soup.find(True, class_="wprm-recipe-ingredients-container")

        if not isinstance(div, Tag):
            return {}

        result = {}

        groups = div.find_all(True, class_="wprm-recipe-ingredient-group")

        for group in groups:
            name_container = group.find(True, class_="wprm-recipe-group-name")
            if name_container:
                name = re.sub(":$", "", text(name_container))
            else:
                name = None

            ingredients = group.select("ul li.wprm-recipe-ingredient")
            for ingredient in ingredients:
                for checkbox in ingredient.find_all(
                    True, class_="wprm-checkbox-container"
                ):
                    checkbox.extract()
            ingredients = [text(li) for li in ingredients]
            result[name] = ingredients

        return result

    def instructions(self) -> SubheadingGroup:
        div = self.soup.find(True, class_="wprm-recipe-instructions-container")

        if not isinstance(div, Tag):
            return {}

        result = {}

        groups = div.find_all(True, class_="wprm-recipe-instruction-group")

        for group in groups:
            name_container = group.find(True, class_="wprm-recipe-group-name")
            if name_container:
                name = re.sub(":$", "", text(name_container))
            else:
                name = None

            instructions = group.select("li.wprm-recipe-instruction")
            for instruction in instructions:
                for checkbox in instruction.find_all(
                    True, class_="wprm-checkbox-container"
                ):
                    checkbox.extract()
            instructions = [text(li) for li in instructions]
            result[name] = instructions

        return result

    def time(self) -> dict[str, str]:
        section = self.extract_one(".wprm-recipe-times-container")

        if section:
            values_tags = section.select(".wprm-recipe-time")
            values = [text(value) for value in values_tags]

            labels_tags = section.select(".wprm-recipe-time-label")
            labels = [
                re.sub(r"( Time)?:?\s*$", "", text(label))
                for label in labels_tags
            ]

            acceptable_labels = ["cook", "prep", "additional", "total", "rest"]
            pairs = {
                label.capitalize(): value
                for label, value in zip(labels, values)
                if label.lower() in acceptable_labels
            }

            return pairs
        return {}

    def notes(self) -> SubheadingGroup:
        div = self.soup.find(True, class_="wprm-recipe-notes")

        if div:
            return {"": [line for line in div.text.split("\n") if line]}

        return {}
