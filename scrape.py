from sys import argv

from bs4 import BeautifulSoup
import requests as r

from handlers import Recipe
from handlers.allrecipes import AllrecipesHandler
from handlers.bbc import BBCHandler
from handlers.delish import DelishHandler
from handlers.epicurious import EpicuriousHandler
from handlers.kingarthur import KingArthurHandler
from handlers.seriouseats import SeriousEatsHandler
from handlers.tasty import TastyHandler
from handlers.wordpress import WordpressHandler
from handlers.wordpress_tasty import WordpressTastyV3Handler


def get_soup(url: str) -> BeautifulSoup:
    """cURL the provided `url`.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:88.0)"
                      "Gecko/20100101 Firefox/88.0"
    }
    req = r.get(url, headers=headers)
    if req.status_code != 200:
        raise Exception(f"Error {req.status_code}")

    raw_html = req.text
    return BeautifulSoup(raw_html, "html.parser")


def from_url(url: str) -> Recipe:
    """Parse a recipe from a given URL.
    """

    handlers = [SeriousEatsHandler,
                AllrecipesHandler,
                KingArthurHandler,
                TastyHandler,
                WordpressHandler,
                WordpressTastyV3Handler,
                BBCHandler,
                DelishHandler
                ]

    soup = get_soup(url)
    for handler in handlers:
        try:
            print(handler)
            recipe = Recipe(soup, handler)
            if recipe.ingredients and recipe.instructions:
                break
        except:  # pylint:disable=bare-except
            pass
    else:
        raise Exception("No usable handler found.")

    return recipe

def __main__():
    recipe = from_url(argv[1])

    print(recipe.title)

    print("INGREDIENTS")
    for name, ings in (recipe.ingredients.items()):
        if name:
            print(f"{name}:")
        for i, ing in enumerate(ings):
            if ing:
                print(f"{i + 1}. {ing}")

    print()
    print("INSTRUCTIONS")
    for name, insts in (recipe.instructions.items()):
        if name:
            print(f"{name}:")
        for i, inst in enumerate(insts):
            if inst:
                print(f"{i + 1}. {inst}")

if __name__ == "__main__":
    __main__()
