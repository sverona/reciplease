import re

from bs4 import NavigableString


def split_into_subheads(list_to_split, regex=r"[^.]+:"):
    subheads = {}
    this_subhead = ''
    for item in list_to_split:
        if re.match(regex, item, re.I):
            this_subhead, this_item = item.split(":", 1)
            subheads[this_subhead] = []
            if this_item:
                subheads[this_subhead].append(this_item.strip())
        else:
            if not subheads:
                this_subhead = ''
                subheads[this_subhead] = []
            subheads[this_subhead].append(item.strip())
    return subheads


class RecipeHandler:
    regexes = {}
    _source = ""

    def __init__(self):
        pass

    def match(self, url: str) -> bool:
        for regex, name in self.regexes.items():
            print(regex, name, url)
            if re.search(regex, url):
                self._source = name
                print(self._source)
                return True
        return False

    def title(self, soup: NavigableString) -> NavigableString:
        return ""

    def time(self, soup: NavigableString) -> NavigableString:
        return ""

    def author(self, soup: NavigableString) -> NavigableString:
        return ""

    def source(self, soup: NavigableString) -> NavigableString:
        return self._source

    def url(self, soup: NavigableString) -> NavigableString:
        return ""

    def active_time(self, soup: NavigableString) -> NavigableString:
        return ""

    def total_time(self, soup: NavigableString) -> NavigableString:
        return ""

    def ingredients(self, soup: NavigableString) -> NavigableString:
        return {'': []}

    def instructions(self, soup: NavigableString) -> NavigableString:
        return {'': []}

    def notes(self, soup: NavigableString) -> NavigableString:
        return ""
