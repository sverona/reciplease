import re
from unicodedata import normalize

from bs4 import Tag

from . import RecipeHandler, SubheadingGroup


class WordpressTastyV3Handler(RecipeHandler):
    """Handler for recipes from WordPress blogs that use Tasty Recipes V3.
    """

    def title(self) -> str:
        heading = self.extract_one(".tasty-recipes-title")

        if heading:
            return heading.text.strip()
        return ""

    def author(self) -> str:
        author_name = self.extract_one(".tasty-recipes-author-name")

        if author_name:
            return author_name.text.strip()
        return ""

    def source(self) -> str:
        site_name = self.soup.find("meta", attrs={"property": "og:site_name"})

        if isinstance(site_name, Tag):
            content = site_name.attrs["content"]
            if isinstance(content, str):
                return content
            return ", ".join(content)
        return ""

    def yield_(self) -> str:
        yield_tag = self.extract_one(".tasty-recipes-yield", remove=".tasty-recipes-yield-scale")

        if yield_tag:
            return yield_tag.text.strip()
        return ""

    def time(self) -> dict[str, str]:
        section = self.extract_one(".tasty-recipes-details")

        if section:
            values_tags = section.find_all(class_=re.compile("tasty-recipes-[a-z]+-time"))
            values = [value.text.strip() for value in values_tags]

            labels_tags = section.select(".tasty-recipes-label")
            labels = [re.sub(" Time:$", "", label.text.strip())
                      for label in labels_tags
                      if re.search(" Time:$", label.text.strip())]

            acceptable_labels = ["Cook", "Prep", "Additional", "Total"]
            pairs = {label: value
                     for label, value in zip(labels, values)
                     if label in acceptable_labels}

            return pairs
        return {}

    def ingredients(self) -> SubheadingGroup:
        ingredients_tags = self.extract(".tasty-recipes-ingredients li")
        ingredients = [li.text.strip() for li in ingredients_tags]
        return {None: ingredients}

    def instructions(self) -> SubheadingGroup:
        instructions_tags = self.extract(".tasty-recipes-instructions li")
        instructions = [li.text.strip() for li in instructions_tags]
        return {None: instructions}

    def notes(self) -> SubheadingGroup:
        notes_tags = self.extract(".tasty-recipes-notes p")
        notes = [p.text.strip() for p in notes_tags]
        return {None: notes}


class WordpressTastyPreV3Handler(RecipeHandler):
    """Handler for recipes from WordPress blogs that use Tasty Recipes pre-V3.
    """

    def title(self) -> str:
        heading = self.extract_one(".tasty-recipes-title")
        if heading:
            return heading.text.strip()
        return ""

    def author(self) -> str:
        author = self.extract_one(".tasty-recipes-author-name")
        if author:
            return author.text.strip()
        return ""

    def source(self) -> str:
        site_name = self.soup.find("meta", attrs={"property": "og:site_name"})

        if isinstance(site_name, Tag):
            content = site_name.attrs["content"]
            if isinstance(content, str):
                return content
            return ", ".join(content)
        return ""

    def yield_(self) -> str:
        yield_ = self.extract_one(".tasty-recipes-yield",
                                  remove=".tasty-recipes-yield-scale")

        if yield_:
            return yield_.text.strip()
        return ""

    def ingredients(self) -> SubheadingGroup:
        # I know of no recipe containing ingredient groups
        ingredients_tags = self.extract(".tasty-recipe-ingredients li")
        ingredients = [li.text.strip() for li in ingredients_tags]
        return {None: ingredients}

    def instructions(self) -> SubheadingGroup:
        instructions_tags = self.extract(".tasty-recipe-instructions li")
        instructions = [li.text.strip() for li in instructions_tags]
        return {None: instructions}

    def notes(self) -> SubheadingGroup:
        notes_tags = self.extract(".tasty-recipes-notes-body", root=".tasty-recipes-notes")
        notes = [normalize("NFKC", p.text.strip()) for p in notes_tags]
        return {None: notes}

    def time(self) -> dict[str, str]:
        section = self.extract_one(".tasty-recipes-details")

        if section:
            values_tags = section.find_all(class_=re.compile("tasty-recipes-[a-z]+-time"))
            values = [value.text.strip() for value in values_tags]

            labels_tags = section.select(".tasty-recipes-label")
            labels = [re.sub(" Time:$", "", label.text.strip())
                      for label in labels_tags
                      if re.search(" Time:$", label.text.strip())]

            acceptable_labels = ["Cook", "Prep", "Additional", "Total"]
            pairs = {label: value
                     for label, value in zip(labels, values)
                     if label in acceptable_labels}

            return pairs
        return {}

