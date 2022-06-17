"""Abstract class for recipe parsers.
"""

from copy import copy
from dataclasses import dataclass
import re
from typing import Iterable
import unicodedata

from bs4 import BeautifulSoup, NavigableString, Tag


SubheadingGroup = dict[str | None, list[str]]

class RecipeHandler:
    """Abstract class for recipe parsers.
    """

    soup: Tag

    def __init__(self, soup: Tag):
        self.soup = soup

    def title(self) -> str:
        """Return the recipe title.
        """
        return ""

    def author(self) -> str:
        """Return the recipe author(s).
        """
        return ""

    def source(self) -> str:
        """Return the title of the website the recipe was posted on.
        """
        return ""

    def time(self) -> dict[str, str]:
        """Return a dict mapping "prep time", "total time", etc. to times
        represented as strings.
        """
        return {}

    def yield_(self) -> str:
        """Return a string containing the recipe yield.
        """
        return ""

    def ingredients(self) -> SubheadingGroup:
        """Return a SubheadingGroup containing recipe ingredients.
        """
        return {}

    def instructions(self) -> SubheadingGroup:
        """Return a SubheadingGroup containing recipe instructions.
        """
        return {}

    def notes(self) -> SubheadingGroup:
        """Return a SubheadingGroup containing recipe notes.
        """
        return {}

    def extract(self,
                keep: str | Iterable[str],
                remove: str | Iterable[str] | None=None,
                root=None
                ) -> list[Tag]:
        """Extract all elements in `self.soup` matching any selector in `keep`,
        limited to children of `self.soup.select_one(root)` if `root` is
        provided, removing any elements matching any selector in `remove`.
        """
        root_element = None
        if not root:
            root_element = copy(self.soup)
        else:
            root_tag = self.soup.select_one(root)
            if root_tag:
                root_element = copy(root_tag)

        if root_element:
            if isinstance(remove, str):
                for to_remove in root_element.select(remove):
                    to_remove.extract()
            elif remove: # remove is Iterable[str]
                for to_remove in root_element.select(",".join(remove)):
                    to_remove.extract()

            if isinstance(keep, str):
                return root_element.select(keep)

            if keep:  # keep is Iterable[str]
                return root_element.select(",".join(keep))

        return []

    def extract_one(self, keep: str | Iterable[str], remove=None, root=None) -> Tag | None:
        """Same as `_extract` but return at most one match.
        """
        elements = self.extract(keep, remove, root)
        if elements:
            return elements[0]
        return None

def text(tag: Tag | NavigableString | None) -> str:
    """Return the normalized, stripped text of an HTML `tag`, or the empty
    string if `tag` is `None`.
    """
    if not tag:
        return ""
    text_ = tag.text.strip()
    if unicodedata.is_normalized("NFKC", text_):
        return text_
    return unicodedata.normalize("NFKC", text_)

def split_into_subheadings(list_to_split: list[str], regex=r"[^.]+:") -> SubheadingGroup:
    """Split a list of strings (say, of instructions or ingredients) which
    may contain subheadings (say, "To make the dough:") into a dict mapping
    those subheadings (or None, for an empty subheading) to the strings they
    belong with.

    The optional `regex` argument specifies the pattern with which to
    determine whether a string begins with a subheading.
    """
    subheads: SubheadingGroup = {}
    this_subhead = None
    for item in list_to_split:
        if re.match(regex, item, re.I):
            this_subhead, this_item = item.split(":", 1)
            subheads[this_subhead] = []
            if this_item:
                subheads[this_subhead].append(this_item.strip())
        else:
            if not subheads:
                this_subhead = None
                subheads[this_subhead] = []
            subheads[this_subhead].append(item.strip())
    return subheads

@dataclass
class Recipe:
    """Data class containing metadata of a recipe.
    """
    title: str
    author: str
    source: str
    time: dict[str, str]
    yield_: str
    ingredients: SubheadingGroup
    instructions: SubheadingGroup
    notes: SubheadingGroup

    def __init__(self, soup: BeautifulSoup, handler_type: type[RecipeHandler]):
        """Attempt to parse a recipe from a given BeautifulSoup object `soup`.
        """

        handler = handler_type(soup)

        self.title = handler.title()
        self.author = handler.author()
        self.source = handler.source()
        self.yield_ = handler.yield_()
        self.time = handler.time()
        self.ingredients = handler.ingredients()
        self.instructions = handler.instructions()
        self.notes = handler.notes()
