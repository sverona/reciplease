from handlers import Page, Recipe
from handlers.delish import DelishHandler


class TestDelish:
    """The Delish handler should..."""

    url = "https://www.delish.com/cooking/recipe-ideas/a40119787/pork-adobo-recipe/"  # noqa:E501
    recipe = Recipe(Page(url), DelishHandler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Pork Adobo"

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "June Xie"

    def test_source(self):
        """...properly scrape the recipe source."""
        assert self.recipe.source == "Delish"

    def test_yield_(self):
        """...properly scrape the recipe yield."""
        assert self.recipe.yield_ == "6 servings"

    def test_ingredient_sections(self):
        """...break ingredients up into sections."""
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...properly scrape ingredients."""
        assert "2 tbsp. fish sauce" in self.recipe.ingredients["Marinade"]

        assert len(self.recipe.ingredients["Marinade"]) == 7

    def test_instruction_sections(self):
        """...break instructions up into sections."""
        assert len(self.recipe.instructions) == 2

    def test_instructions(self):
        """...properly scrape instructions."""
        assert (
            "Place rice on a platter. Top with pork and pour sauce over."
            in self.recipe.instructions["Adobo And Assembly"]
        )

        assert len(self.recipe.instructions["Adobo And Assembly"]) == 4

    def test_time(self):
        """...properly convert times into a dict."""
        expected = {"Prep": "0 hours 25 mins", "Total": "2 hours 0 mins"}
        assert self.recipe.time == expected

    # I was unable to find a Delish recipe containing a notes section.


class TestDelishOnGoodHousekeeping:
    """When run on Good Housekeeping, the Delish handler should..."""

    url = "https://www.goodhousekeeping.com/food-recipes/healthy/a30729432/spring-green-salad-apricot-vinaigrette-recipe/"  # noqa:E501
    recipe = Recipe(Page(url), DelishHandler)

    def test_title(self):
        """...scrape the title."""
        assert (
            self.recipe.title == "Spring Salad Recipe With Apricot Vinaigrette"
        )

    def test_author(self):
        """...scrape the author."""
        assert self.recipe.author == "The Good Housekeeping Test Kitchen"

    def test_source(self):
        """...scrape the source."""
        assert self.recipe.source == "Good Housekeeping"

    def test_yield(self):
        """...scrape the yield."""
        assert self.recipe.yield_ == "8 servings"

    def test_time(self):
        """...parse times into a dict."""
        assert self.recipe.time == {"Total": "0 hours 20 mins"}

    # I was unable to find a Good Housekeeping recipe with ingredient or
    # instruction sections.

    def test_ingredients(self):
        """...scrape the ingredients."""
        assert "2 tbsp. olive oil" in self.recipe.ingredients[None]

        assert len(self.recipe.ingredients[None]) == 11

    def test_instructions(self):
        """...scrape the instructions."""
        assert (
            "Toss together remaining ingredients, then toss with vinaigrette."
            in self.recipe.instructions[None]
        )

        assert len(self.recipe.instructions[None]) == 3
