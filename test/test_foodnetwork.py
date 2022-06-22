from handlers import Page, Recipe
from handlers.foodnetwork import FoodNetworkHandler


class TestFoodNetwork:
    """The Food Network handler should..."""

    url = "https://www.foodnetwork.com/recipes/trisha-yearwood/zucchini-cakes-with-herb-sour-cream-1-7118338"
    recipe = Recipe(Page(url), FoodNetworkHandler)

    def test_title(self):
        """...scrape the title."""
        assert self.recipe.title == "Zucchini Cakes with Herb Sour Cream"

    def test_author(self):
        """...scrape the author."""
        assert self.recipe.author == "Trisha Yearwood"

    def test_source(self):
        """...scrape the source."""
        assert self.recipe.source == "Food Network"

    def test_yield_(self):
        """...scrape the yield."""
        assert self.recipe.yield_ == "6 to 8 servings"

    def test_time(self):
        """...parse times into a dict."""
        expected = {"Total": "40 min", "Active": "20 min"}
        assert self.recipe.time == expected

    def test_ingredient_sections(self):
        """...break up ingredients into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...scrape the ingredients."""
        assert "4 large eggs" in self.recipe.ingredients["Zucchini Cakes"]
        assert len(self.recipe.ingredients["Zucchini Cakes"]) == 10

    def test_instructions(self):
        """...scrape the instructions."""
        assert (
            "Make the herb sour cream: Whisk the sour cream, chives and dill"
            " in a medium bowl. Set aside."
            in self.recipe.instructions[None]
        )

        assert len(self.recipe.instructions[None]) == 3
