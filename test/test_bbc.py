from handlers import Page, Recipe
from handlers.bbc import BBCHandler


class TestBBC:
    """The BBC handler should..."""

    url = "https://www.bbcgoodfood.com/recipes/red-lentil-pasta-with-creamy-tomato-pepper-sauce"
    recipe = Recipe(Page(url), BBCHandler)

    def test_title(self):
        """...properly scrape the title."""
        assert (
            self.recipe.title
            == "Red lentil pasta with creamy tomato & pepper sauce"
        )

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "Sara Buenfeld"

    def test_source(self):
        """...properly scrape the recipe source."""
        assert self.recipe.source == "BBC Good Food"

    def test_yield_(self):
        """...properly scrape the recipe yield."""
        assert self.recipe.yield_ == "2"

    def test_ingredient_sections(self):
        """...break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...properly scrape ingredients."""
        assert (
            "4 sundried tomatoes" in self.recipe.ingredients["For the sauce"]
        )

    def test_instructions(self):
        """...properly scrape instructions."""
        assert (
            "Drain the pasta, mix with the sauce in a large bowl, then divide"
            " between two bowls and add a handful of rocket to each."
            in self.recipe.instructions[None]
        )

    def test_time(self):
        """...properly convert times into a dict."""
        expected = {"Prep": "10 mins", "Cook": "8 mins"}
        assert self.recipe.time == expected

    # I was unable to find a BBC recipe containing a notes section.
