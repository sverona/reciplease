from handlers import Page, Recipe
from handlers.tasty import TastyHandler


class TestTasty:
    """The Tasty handler should..."""

    url = "https://tasty.co/recipe/ritu-swasti-s-shahi-paneer"
    recipe = Recipe(Page(url), TastyHandler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Shahi Paneer"

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "Rie McClenny"

    def test_source(self):
        """...properly scrape the recipe source."""
        assert self.recipe.source == "Tasty"

    # tasty.co doesn't provide recipe timings yet.

    def test_yield(self):
        """...properly scrape the recipe yield."""
        assert self.recipe.yield_ == "4 servings"

    def test_ingredients(self):
        """...properly scrape ingredients."""
        assert (
            "1 tablespoon ginger, crushed" in self.recipe.ingredients["Paneer"]
        )
        assert len(self.recipe.ingredients["For Serving"]) == 3

    def test_ingredient_sections(self):
        """...properly break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_instructions(self):
        """...properly scrape instructions."""
        assert "Enjoy!" in self.recipe.instructions[None]
        assert len(self.recipe.instructions[None]) == 7

    # I was unable to find a tasty.co recipe that included notes.
