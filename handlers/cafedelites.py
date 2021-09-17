import re

from bs4 import NavigableString

from .wordpress import WordpressHandler


class CafeDelitesHandler(WordpressHandler):
    regex = r"cafedelites\.com"

    def __init__(self):
        super().__init__()

    def source(self, soup: NavigableString) -> NavigableString:
        return "Cafe Delites"
