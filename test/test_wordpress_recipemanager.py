from scrape import from_url


class TestWordpressRecipeManager:
    """The Wordpress Recipe Manager handler should...
    """

    url = "https://www.cookwithmanali.com/moong-dal-dosa/"
    recipe = from_url(url)

    def test_title(self):
        """...properly scrape the title.
        """
        assert self.recipe.title == "Moong Dal Dosa"

    def test_ingredient_sections(self):
        """...break ingredients up into sections.
        """
        assert len(self.recipe.ingredients.keys()) == 2

    def test_ingredients(self):
        """...properly scrape ingredients.
        """
        assert "1 inch ginger" in self.recipe.ingredients[None]
        assert "7-8 curry leaves" in self.recipe.ingredients['Paneer filling']

    def test_instruction_sections(self):
        """...break instructions up into sections.
        """

        assert len(self.recipe.instructions.keys()) == 2

    def test_instructions(self):
        """...properly scrape instructions.
        """

        assert "Once soaked for 3 hours, drain the dal using a colander and rinse it well." in self.recipe.instructions['Make the dosa']
