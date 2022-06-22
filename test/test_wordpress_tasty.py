from handlers import Page, Recipe
from handlers.wordpress_tasty import (
    WordpressTastyV3Handler,
    WordpressTastyPreV3Handler,
)


class TestWordpressTastyV3:
    """The Wordpress Tasty V3 handler should..."""

    url = "https://www.wptasty.com/tasty-recipes/demo"
    recipe = Recipe(Page(url), WordpressTastyV3Handler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "Tasty Sourdough Bread"

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "Katie Koteen"

    def test_source(self):
        """...properly scrape the recipe source."""
        assert self.recipe.source == "WP Tasty"

    def test_time(self):
        """...properly convert recipe times into a dict."""
        expected = {
            "Prep": "1 hour",
            "Cook": "30 minutes",
            "Total": "1 hour 30 minutes",
        }
        assert self.recipe.time == expected

    def test_yield(self):
        """...properly scrape the recipe yield."""
        assert self.recipe.yield_ == "10 servings"

    def test_ingredients(self):
        """...properly scrape ingredients."""
        assert "3 cups all purpose flour" in self.recipe.ingredients[None]

    def test_instructions(self):
        """...properly scrape instructions."""
        assert (
            "DOUGH PREP: In a large mixing bowl, whisk the flour, salt, and yeast together until mixed. Stir in the water until a chunky, thick dough forms. Let it rest, like maybe forever."
            in self.recipe.instructions[None]
        )

    def test_notes(self):
        """...properly scrape recipe notes."""
        assert (
            "The equipment section above contains affiliate links to products we use and love!"
            in self.recipe.notes[None]
        )


class TestWordpressTastyPreV3:
    """The Wordpress Tasty pre-V3 handler should..."""

    # This was a bitch to find.
    # https://support.wptasty.com/en/articles/805141-can-i-use-a-custom-php-template
    url = "https://www.wickedstuffed.com/keto-recipes/low-carb-keto-pancakes-recipe-with-cream-cheese/"
    recipe = Recipe(Page(url), WordpressTastyPreV3Handler)

    url2 = "https://cookieandkate.com/best-red-chilaquiles-recipe/"
    recipe2 = Recipe(Page(url2), WordpressTastyPreV3Handler)

    def test_title(self):
        """...properly scrape the title."""
        assert self.recipe.title == "The Original Keto Pancakes Recipe"

    def test_title_unclassed(self):
        """...properly scrape titles not possessing a class."""
        assert self.recipe2.title == "Chilaquiles Rojos"

    def test_author(self):
        """...properly scrape the author."""
        assert self.recipe.author == "Amanda C. Hughes"

    def test_source(self):
        """...properly scrape the source."""
        assert self.recipe.source == "WickedStuffed: A Keto Recipe Blog"

    def test_time(self):
        """...properly parse times into a dict."""
        expected = {
            "Prep": "2 minutes",
            "Cook": "5 minutes",
            "Total": "7 minutes",
        }
        assert self.recipe.time == expected

    def test_yield(self):
        """...properly scrape the yield."""
        assert self.recipe.yield_ == "1 Serving"

    def test_ingredients(self):
        """...properly scrape the ingredients."""
        assert "2 eggs" in self.recipe.ingredients[None]

    def test_instructions(self):
        """...properly scrape the instructions."""
        assert (
            "Blend or beat together all of the ingredients until smooth in a bowl or blender."
            in self.recipe.instructions[None]
        )

    def test_notes(self):
        """...properly scrape the notes."""
        assert (
            "The coconut flour in this keto pancakes recipe helps keep the pancakes together, rather than crumbling like almond flour tends to do. It also helps them crisp up in the pan. I really like Lakanto’s Monkfruit Maple Syrup (use code WICKEDSTUFFED to save 20%)"
            in self.recipe.notes[None]
        )
