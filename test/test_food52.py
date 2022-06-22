from handlers import Page, Recipe
from handlers.food52 import Food52Handler


class TestFood52:
    """The Food52 handler should..."""

    url = (
        "https://food52.com/recipes/34010-soba-with-parsley-pea-pesto-and-kale"
    )
    recipe = Recipe(Page(url), Food52Handler)

    def test_title(self):
        """...scrape the title."""
        assert self.recipe.title == "Soba with Parsley-Pea Pesto and Kale"

    def test_author(self):
        """...scrape the author."""
        assert self.recipe.author == "Kim Sanz"

    def test_source(self):
        """...scrape the source."""
        assert self.recipe.source == "Food52"

    def test_yield(self):
        """...scrape the yield."""
        assert self.recipe.yield_ == "Serves 2"

    def test_ingredient_sections(self):
        """...break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...scrape the ingredients."""
        assert "Salt, to taste" in self.recipe.ingredients["Soba with kale"]

    def test_instruction_sections(self):
        """...break instructions up into sections."""
        assert len(self.recipe.instructions) == 2

    def test_instructions(self):
        """...scrape the instructions."""
        assert (
            "Once noodles and peas are cooked, drain both and return to the"
            " pot. Add chopped kale and pesto. Toss to coat evenly. You're"
            " done! Enjoy!"
            in self.recipe.instructions["Soba with kale"]
        )

    # Could not find a Food52 recipe with a time section.
