from handlers import Recipe
from handlers.tasty import TastyHandler
from scrape import get_soup


class TestTasty:
    """The Tasty handler should..."""

    url = "https://tasty.co/recipe/ritu-swasti-s-shahi-paneer"
    recipe = Recipe(get_soup(url), TastyHandler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Shahi Paneer"

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "Rie McClenny"

    def test_source(self):
        """...properly scrape the recipe source."""
        assert self.recipe.source == "tasty.co"

    # tasty.co doesn't provide recipe timings yet.

    def test_yield(self):
        """...properly scrape the recipe yield."""
        assert self.recipe.yield_ == "4 servings"

    def test_ingredients(self):
        """...properly scrape ingredients."""
        assert (
            "1 tablespoon ginger, crushed" in self.recipe.ingredients["Paneer"]
        )

    def test_ingredient_sections(self):
        """...properly break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_instructions(self):
        """...properly scrape instructions."""
        assert "Enjoy!" in self.recipe.instructions[None]

    # I was unable to find a tasty.co recipe that included notes.
