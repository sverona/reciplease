from typing import Type

from bs4 import BeautifulSoup
import pytest

from handlers import Page, Recipe, RecipeHandler
from handlers.all import ALL_HANDLERS


class TestNegative:
    """Checking for correct negative responses:"""

    @pytest.mark.parametrize("handler", [RecipeHandler] + ALL_HANDLERS)
    def test_handler_for_correct_negative_response(
        self, handler: Type[RecipeHandler]
    ):
        empty_soup = BeautifulSoup("<html></html>", features="lxml")
        page = Page("", soup=empty_soup)

        nothing = Recipe(page, handler)

        assert nothing.title == ""
        assert nothing.author == ""
        assert nothing.source == ""
        assert nothing.yield_ == ""

        assert not nothing.time
        assert not nothing.ingredients
        assert not nothing.instructions
        assert not nothing.notes
