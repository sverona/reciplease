from handlers import Page, Recipe
from handlers.kingarthur import KingArthurHandler


class TestKingArthur:
    """The King Arthur Baking handler should..."""

    url = "https://www.kingarthurbaking.com/recipes/lemon-bliss-cake-recipe"
    recipe = Recipe(Page(url), KingArthurHandler)

    def test_ingredient_sections(self):
        """...break ingredients up by section."""

        assert len(self.recipe.ingredients.items()) == 3

    def test_ingredients(self):
        """...properly scrape ingredients."""

        assert "1 teaspoon salt" in self.recipe.ingredients["Cake"]

    def test_instructions(self):
        """...properly scrape instructions."""

        assert (
            "Allow the cake to cool completely before icing and serving."
            in self.recipe.instructions[None]
        )

    def test_instruction_sections(self):
        """...break up ingredients into sections."""
        assert len(self.recipe.instructions.items()) == 2

    def test_notes(self):
        """...properly scrape notes."""

        assert (
            "For stronger lemon flavor, use the grated rind of 2 lemons + 1/2"
            " teaspoon lemon oil."
            in self.recipe.notes[None]
        )

    def test_author(self):
        """...properly scrape the author."""

        assert self.recipe.author == "PJ Hamel"

    def test_yield(self):
        """...properly scrape the yield."""

        assert self.recipe.yield_ == "one Bundt cake"

    def test_footnotes(self):
        """...catch footnotes in the ingredients section."""

        assert (
            "*If you use salted butter, reduce the salt in the recipe to 3/4"
            " teaspoon."
            in self.recipe.notes[None]
        )

    def test_time(self):
        """...parse the times into a dict properly."""

        assert self.recipe.time == {
            "Prep": "20 mins",
            "Bake": "45 mins to 1 hr",
            "Total": "1 hr 20 mins",
        }
