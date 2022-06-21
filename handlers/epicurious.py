import re

from bs4 import Tag

from . import RecipeHandler, SubheadingGroup, split_into_subheadings, text


class EpicuriousHandler(RecipeHandler):
    """Handler for recipes from epicurious.com."""

    # I swear to fuck...
    def title(self) -> str:
        tag = self.soup.find("h1", {"data-testid": "ContentHeaderHed"})
        return text(tag)

    def author(self) -> str:
        tag = self.soup.find("span", {"data-testid": "BylineName"})
        return re.sub("^By ", "", text(tag))

    def source(self) -> str:
        return "Epicurious"

    def yield_(self) -> str:
        tag = self.soup.find(class_=re.compile("^Yield.*"))
        return re.sub("^Makes ", "", text(tag))

    def ingredients(self) -> SubheadingGroup:
        container = self.soup.find("div", {"data-testid": "IngredientList"})
        if not isinstance(container, Tag):
            return {}

        tag = container.find(class_=re.compile("^List.*"))
        if not isinstance(tag, Tag):
            return {}

        tag_list = [text(t) for t in tag.find_all("div")]
        return split_into_subheadings(tag_list)

    def instructions(self) -> SubheadingGroup:
        instructions = {}

        sections = self.soup.find_all(class_=re.compile("^InstructionGroupWrapper.*"))
        for section in sections:
            title = re.sub(":$", "", text(section.h3)) or None
            these_instructions = section.find_all(
                class_=re.compile("^InstructionBody.*")
            )
            instructions[title] = [text(ins) for ins in these_instructions]

        return instructions

    def time(self) -> dict[str, str]:
        times = {}

        containers = self.soup.find_all(class_=re.compile("^InfoSliceItem.*"))
        for container in containers:
            name = text(container.find(class_=re.compile("^InfoSliceKey.*")))
            name = re.sub(" Time$", "", name)

            time = text(container.find(class_=re.compile("^InfoSliceValue.*")))
            times[name] = time

        return times
