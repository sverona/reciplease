import re

from . import RecipeHandler, SubheadingGroup

class AllrecipesHandler(RecipeHandler):
    """Handler for recipes from allrecipes.com.
    """

    def title(self) -> str:
        tag = self.extract_one("h1", root=".recipe-main-header")
        if tag:
            return tag.text.strip()
        return ""

    def source(self) -> str:
        return "Allrecipes"

    def ingredients(self) -> SubheadingGroup:
        sections = self.extract(".ingredients-section__fieldset")

        headings: list[str | None] = []
        for section in sections:
            heading_tag = RecipeHandler(section).extract_one(".ingredients-section__legend")
            if heading_tag:
                heading_text = heading_tag.text.strip()
                heading_text = re.sub("^For the ", "", heading_text)
                heading_text = re.sub(":$", "", heading_text)
                headings.append(heading_text)
            else:
                headings.append(None)

        ingredients: SubheadingGroup = {}
        for heading, section in zip(headings, sections):  # type: ignore
            these_ingredients = RecipeHandler(section).extract("li")
            ingredients[heading] = [ing.text.strip() for ing in these_ingredients if ing]

        return ingredients

    def instructions(self) -> SubheadingGroup:
        # I was unable to find a recipe on this site with distinct sections or section headings.
        # If you find one, please open a PR. SVM
        steps_tags = self.extract(".section-body", root=".instructions-section")
        steps = [step.text.strip() for step in steps_tags]

        return {None: steps}

    def yield_(self) -> str:
        values_tags = self.extract(".recipe-meta-item-body", root=".recipe-meta-container")
        labels_tags = self.extract(".recipe-meta-item-header", root=".recipe-meta-container")

        values = [value.text.strip() for value in values_tags]
        labels = [re.sub(":$", "", label.text.strip()) for label in labels_tags]

        pairs = {label.capitalize(): value for label, value in zip(labels, values)}

        if "Yield" in pairs.keys():
            return pairs["Yield"]
        if "Servings" in pairs.keys():
            return pairs["Servings"]
        return ""

    def time(self) -> dict[str, str]:
        values_tags = self.extract(".recipe-meta-item-body", root=".recipe-meta-container")
        labels_tags = self.extract(".recipe-meta-item-header", root=".recipe-meta-container")

        values = [value.text.strip() for value in values_tags]
        labels = [re.sub(":$", "", label.text.strip()) for label in labels_tags]

        accept = ["cook", "prep", "additional", "total"]
        pairs = {label.capitalize(): value
                 for label, value in zip(labels, values)
                 if label in accept}

        return pairs

    def notes(self) -> SubheadingGroup:
        sections = self.extract(".recipe-note", root=".recipe-notes")

        headings: list[str | None] = []
        notes = []
        for section in sections:
            handler = RecipeHandler(section)
            tag = handler.extract_one("h2")
            if tag:
                headings.append(re.sub(":$", "", tag.text.strip()))
            else:
                headings.append(None)

            notes_tags = handler.extract(".paragraph")
            notes.append([note.text.strip() for note in notes_tags])

        return dict(zip(headings, notes))

    def author(self) -> str:
        author_tag = self.extract_one(".author-name")
        if author_tag:
            return author_tag.text.strip()
        return ""
