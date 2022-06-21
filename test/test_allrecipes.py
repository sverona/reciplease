from scrape import from_url


class TestAllrecipes:
    """The AllRecipes handler should..."""

    url = "https://www.allrecipes.com/recipe/281437/chef-johns-taco-stuffed-zucchini-boats/"
    recipe = from_url(url)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Chef John's Taco-Stuffed Zucchini Boats"

    def test_ingredient_sections(self):
        """...break ingredients up into sections."""
        assert len(self.recipe.ingredients.keys()) == 2

    def test_ingredients(self):
        """...properly scrape ingredients."""

        assert (
            "1 cup tomato sauce"
            in self.recipe.ingredients["Taco Meat Stuffing"]
        )
        assert (
            "4 large zucchini, halved lengthwise"
            in self.recipe.ingredients["Rest"]
        )

    def test_instructions(self):
        """...properly scrape instructions."""
        assert (
            "Meanwhile, preheat the oven to 400 degrees F (200 degrees C). Line a baking sheet with a silicone liner."
            in self.recipe.instructions[None]
        )

    def test_notes(self):
        """...properly scrape recipe notes."""
        assert (
            "You can cook these for less time if you prefer a firmer zucchini texture."
            in self.recipe.notes["Chef's Notes"]
        )

    def test_time(self):
        """...properly convert times into a dict."""
        # TODO Do we care about minutes/hours+minutes?

        assert self.recipe.time == {
            "Prep": "30 mins",
            "Cook": "40 mins",
            "Additional": "15 mins",
            "Total": "1 hr 25 mins",
        }

    def test_author(self):
        """...properly scrape the author."""

        assert self.recipe.author == "Chef John"

    def test_yield(self):
        """...properly scrape the yield."""

        assert self.recipe.yield_ == "8 zucchini boats"
