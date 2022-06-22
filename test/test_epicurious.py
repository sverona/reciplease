from handlers import Page, Recipe
from handlers.epicurious import EpicuriousHandler


class TestEpicurious:
    """The Epicurious handler should..."""

    url = "https://www.epicurious.com/recipes/food/views/glazed-cinnamon-cardamom-buns"
    recipe = Recipe(Page(url), EpicuriousHandler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Glazed Cinnamon-Cardamom Buns"

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "Kat Boytsova"

    def test_source(self):
        """...properly scrape the source."""
        assert self.recipe.source == "Epicurious"

    def test_yield_(self):
        """...properly scrape the yield."""
        assert self.recipe.yield_ == "8"

    def test_ingredient_sections(self):
        """...break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...properly scrape the ingredients."""
        assert "1 large egg" in self.recipe.ingredients["For the Dough"]

    def test_instruction_sections(self):
        """...break instructions up into sections."""
        assert len(self.recipe.instructions) == 2

    def test_instructions(self):
        """...properly scrape the instructions."""
        assert (
            "Mix butter, cinnamon, and 1/2 cup brown sugar in a medium bowl"
            " until combined."
            in self.recipe.instructions["For the Filling and Assembly"]
        )

    def test_time(self):
        """...properly parse the times into a dict."""
        expected = {
            "Active": "1 hour 10 minutes",
            "Total": "5 hours 20 minutes, plus an overnight proof",
        }

        assert self.recipe.time == expected
