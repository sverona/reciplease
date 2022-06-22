import re

from . import RecipeHandler, split_into_subheadings, SubheadingGroup, text


class KingArthurHandler(RecipeHandler):
    """Handler for recipes from kingarthurbaking.com."""

    sites = {"kingarthurbaking.com": "King Arthur Baking"}

    def title(self) -> str:
        header = self.extract_one("h1", root="page-content-header")
        return text(header)

    def author(self) -> str:
        author = self.extract_one(".article__author")
        return re.sub(r"^By\s+", "", text(author))

    def ingredients(self) -> SubheadingGroup:
        ingredients = {}
        subheads = self.extract(
            ".ingredient-section", root=".ingredients-list"
        )
        for subhead in subheads:
            paragraph = subhead.find("p")
            if paragraph:
                title = text(paragraph)
            else:
                title = None
            ingredients[title] = [text(li) for li in subhead("li")]
        return ingredients

    def instructions(self) -> SubheadingGroup:
        instructions_tags = self.extract(
            ["ol li", "ul li"],
            remove=["li aside", "share"],
            root=".field--recipe-steps",
        )
        instructions = [text(li) for li in instructions_tags]
        return split_into_subheadings(instructions)

    def yield_(self) -> str:
        span = self.extract_one(".stat__item--yield span")
        return text(span)

    def time(self) -> dict[str, str]:
        times_tags = self.extract(".stat__item span", root=".stats--recipe")
        labels_tags = self.extract(".stat__item .label", root=".stats--recipe")

        labels = [text(label) for label in labels_tags]
        times = [text(time) for time in times_tags]

        return dict(zip(labels, times))

    def notes(self) -> SubheadingGroup:
        notes_tags = self.extract(
            [".recipe__tips ul li", ".ingredient-section__footnote"]
        )
        notes = [text(note) for note in notes_tags]

        if not notes:
            return {}
        return {None: notes}
