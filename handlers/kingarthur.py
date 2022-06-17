import re

from . import RecipeHandler, split_into_subheadings, SubheadingGroup


class KingArthurHandler(RecipeHandler):
    """Handler for recipes from kingarthurbaking.com.
    """

    def title(self) -> str:
        header = self.extract_one("h1", root="page-content-header")

        if header:
            return header.text.strip()
        return ""

    def author(self) -> str:
        author = self.extract_one(".article__author")
        if author:
            return re.sub(r"^By\s+", "", author.text).strip()
        return ""

    def source(self) -> str:
        return "King Arthur Baking"

    def ingredients(self) -> SubheadingGroup:
        ingredients = {}
        subheads = self.extract(".ingredient-section", root=".ingredients-list")
        for subhead in subheads:
            paragraph = subhead.find("p")
            if paragraph:
                title = paragraph.text
            else:
                title = None
            ingredients[title] = [li.text.strip() for li in subhead("li")]
        return ingredients

    def instructions(self) -> SubheadingGroup:
        instructions_tags = self.extract(["ol li", "ul li"],
                                         remove=["li aside", "share"],
                                         root=".field--recipe-steps")
        instructions = [li.text.strip() for li in instructions_tags]
        return split_into_subheadings(instructions)

    def yield_(self) -> str:
        span = self.extract_one(".stat__item--yield span")
        if span:
            return span.text.strip()
        return ""

    def time(self) -> dict[str, str]:
        times_tags = self.extract(".stat__item span", root=".stats--recipe")
        labels_tags = self.extract(".stat__item .label", root=".stats--recipe")

        labels = [label.text.strip() for label in labels_tags]
        times = [time.text.strip() for time in times_tags]

        return dict(zip(labels, times))

    def notes(self) -> SubheadingGroup:
        notes_tags = self.extract([".recipe__tips ul li", ".ingredient-section__footnote"])
        notes = [note.text.strip() for note in notes_tags]

        return {'Notes': notes}
