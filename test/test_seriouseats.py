from scrape import url_to_recipe


class TestSeriousEats:
    """The Serious Eats handler should...
    """
    url = "https://www.seriouseats.com/creamy-cucumber-salad-5196314"
    recipe = url_to_recipe(url)

    def test_ingredients(self):
        """...properly scrape ingredients.
        """

        assert "1 tablespoon (15g) tahini paste" in self.recipe.ingredients['']

    def test_instructions(self):
        """...properly scrape instructions.
        """
        assert "Add cucumber spears and toss until evenly coated with sauce. Transfer to a serving plate, garnish with dill, and serve." in self.recipe.instructions['']

    def test_notes(self):
        """...properly scrape notes.
        """

        assert "To substitute English or cocktail cucumbers, replace with an equal amount by weight. Trim ends and cut into 3- by 5/8-inch wide spears." in self.recipe.notes['Notes']
        assert "Tahini sauce can be prepared in advance and refrigerated in an airtight container for up to 1 week." in self.recipe.notes['Make-ahead and Storage']

    def test_author(self):
        """...properly scrape the author.
        """

        assert self.recipe.author == "Arlyn Osborne"

    def test_yield(self):
        """...properly scrape the yield.
        """

        assert self.recipe.yield_ == "4 servings"

    def test_time(self):
        """...parse the times into a dict properly.
        """

        assert self.recipe.time == {
               "Prep": "45 mins",
               "Total": "45 mins"
               }
