from handlers import Recipe
from handlers.delish import DelishHandler 

from scrape import get_soup


class TestDelish:
    """The Delish handler should...
    """

    url = "https://www.delish.com/cooking/recipe-ideas/a40119787/pork-adobo-recipe/"
    recipe = Recipe(get_soup(url), DelishHandler)

    def test_title(self):
        """...properly scrape the title.
        """
        assert self.recipe.title == "Pork Adobo"

    def test_author(self):
        """...properly scrape the author.
        """
        assert self.recipe.author == "June Xie"

    def test_source(self):
        """...properly scrape the recipe source.
        """
        assert self.recipe.source == "Delish"

    def test_yield_(self):
        """...properly scrape the recipe yield.
        """
        assert self.recipe.yield_ == "6 servings"

    def test_ingredient_sections(self):
        """...break ingredients up into sections.
        """
        assert len(self.recipe.ingredients) == 2

    def test_ingredients(self):
        """...properly scrape ingredients.
        """
        assert "2 tbsp. fish sauce" in self.recipe.ingredients["Marinade"]

    def test_instruction_sections(self):
        """...break instructions up into sections.
        """
        assert len(self.recipe.instructions) == 2

    def test_instructions(self):
        """...properly scrape instructions.
        """
        assert "Place rice on a platter. Top with pork and pour sauce over." in self.recipe.instructions["Adobo And Assembly"]

    def test_time(self):
        """...properly convert times into a dict.
        """
        expected = {"Prep": "0 hours 25 mins", "Total": "2 hours 0 mins"}
        assert self.recipe.time == expected

    # I was unable to find a Delish recipe containing a notes section.
