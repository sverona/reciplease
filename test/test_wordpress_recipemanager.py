from handlers import Page, Recipe
from handlers.wordpress import WordpressHandler


class TestWordpressRecipeManager:
    """The Wordpress Recipe Manager handler should..."""

    url = "https://www.cookwithmanali.com/kadai-paneer/"
    recipe = Recipe(Page(url), WordpressHandler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Kadai Paneer"

    def test_ingredient_sections(self):
        """...break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...properly scrape ingredients."""
        assert "3 cloves" in self.recipe.ingredients["Kadai Masala"]

    def test_instruction_sections(self):
        """...break instructions up into sections."""
        assert len(self.recipe.instructions) == 2

    def test_instructions(self):
        """...properly scrape instructions."""
        assert (
            "Crush kasuri methi and add to the pan."
            in self.recipe.instructions["Make the Kadai Paneer"]
        )

    def test_time(self):
        """...properly parse times into a dict."""
        expected = {"Prep": "15 mins", "Cook": "25 mins", "Total": "40 mins"}
        assert self.recipe.time == expected

    def test_yield(self):
        """...properly scrape the recipe yield."""
        assert self.recipe.yield_ == "4 servings"
