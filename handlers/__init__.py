"""Abstract class for recipe parsers.
"""

from copy import copy
from dataclasses import dataclass
import re
from typing import Iterable, Optional, Union
from urllib.parse import ParseResult as URL, urlparse
import unicodedata

from bs4 import BeautifulSoup, NavigableString, Tag
import requests as r


SubheadingGroup = dict[Optional[str], list[str]]
OneOrMoreStrings = Union[str, Iterable[str]]


@dataclass
class Page:
    """Wrapper class that bundles a URL with its BeautifulSoup tree."""

    url: URL
    soup: Tag

    def __init__(self, url: str, soup: Optional[BeautifulSoup] = None):
        self.url = urlparse(url)

        if self.url.scheme and self.url.netloc:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:88.0)"
                    "Gecko/20100101 Firefox/88.0"
                )
            }
            resp = r.get(url, headers=headers)
            resp.raise_for_status()

        if not soup:
            self.soup = BeautifulSoup(resp.text, "html.parser")
        else:
            self.soup = soup


class RecipeHandler:
    """Abstract class for recipe parsers."""

    page: Page
    sites: dict[str, str] = {}

    def __init__(self, page: Page):
        self.page = page

    def title(self) -> str:
        """Return the recipe title."""
        return ""

    def author(self) -> str:
        """Return the recipe author(s)."""
        return ""

    def source(self) -> str:
        """Return the title of the website the recipe was posted on."""
        for url, title in self.sites.items():
            if url in self.page.url.netloc:
                return title

        site_name = self.page.soup.find(
            "meta", attrs={"property": "og:site_name"}
        )

        if isinstance(site_name, Tag):
            content = site_name.attrs["content"]
            return content
        return ""

    def time(self) -> dict[str, str]:
        """Return a dict mapping "prep time", "total time", etc. to times
        represented as strings.
        """
        return {}

    def yield_(self) -> str:
        """Return a string containing the recipe yield."""
        return ""

    def ingredients(self) -> SubheadingGroup:
        """Return a SubheadingGroup containing recipe ingredients."""
        return {}

    def instructions(self) -> SubheadingGroup:
        """Return a SubheadingGroup containing recipe instructions."""
        return {}

    def notes(self) -> SubheadingGroup:
        """Return a SubheadingGroup containing recipe notes."""
        return {}

    def extract(
        self,
        keep: OneOrMoreStrings,
        remove: Optional[OneOrMoreStrings] = None,
        root=None,
    ) -> list[Tag]:
        """Extract all elements in `self.soup` matching any selector in `keep`,
        limited to children of `self.soup.select_one(root)` if `root` is
        provided, removing any elements matching any selector in `remove`.
        """
        root_element = None
        if not root:
            root_element = copy(self.page.soup)
        else:
            root_tag = self.page.soup.select_one(root)
            if root_tag:
                root_element = copy(root_tag)

        if root_element:
            if isinstance(remove, str):
                for to_remove in root_element.select(remove):
                    to_remove.extract()
            elif remove:  # remove is Iterable[str]
                for to_remove in root_element.select(",".join(remove)):
                    to_remove.extract()

            if isinstance(keep, str):
                return root_element.select(keep)

            if keep:  # keep is Iterable[str]
                return root_element.select(",".join(keep))

        return []

    def extract_one(
        self, keep: OneOrMoreStrings, remove=None, root=None
    ) -> Optional[Tag]:
        """Same as `_extract` but return at most one match."""
        elements = self.extract(keep, remove, root)
        if elements:
            return elements[0]
        return None


def text(tag: Union[Tag, NavigableString, None], squeeze: bool = False) -> str:
    """Return the normalized, stripped text of an HTML `tag`, or the empty
    string if `tag` is `None`.

    The optional `squeeze` argument replaces all contiguous strings of
    whitespace with single spaces if true.
    """
    if not tag:
        return ""
    text_ = tag.text.strip()
    if squeeze:
        text_ = re.sub(r"\s+", " ", text_)
    if unicodedata.is_normalized("NFKC", text_):
        return text_
    return unicodedata.normalize("NFKC", text_)


def split_into_subheadings(
    list_to_split: list[str], regex=r"[^.]+:"
) -> SubheadingGroup:
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
    """Data class containing metadata of a recipe."""

    title: str
    author: str
    source: str
    time: dict[str, str]
    yield_: str
    ingredients: SubheadingGroup
    instructions: SubheadingGroup
    notes: SubheadingGroup

    def __init__(self, page: Page, handler_type: type[RecipeHandler]):
        """Attempt to parse a recipe from a given BeautifulSoup object `soup`."""

        handler = handler_type(page)

        self.title = handler.title()
        self.author = handler.author()
        self.source = handler.source()
        self.yield_ = handler.yield_()
        self.time = handler.time()
        self.ingredients = handler.ingredients()
        self.instructions = handler.instructions()
        self.notes = handler.notes()
