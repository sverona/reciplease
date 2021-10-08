from dataclasses import dataclass, field
from re import sub
from sys import argv

from bs4 import BeautifulSoup
import requests as r

from typing import List, Tuple

from handlers.seriouseats import SeriousEatsHandler
from handlers.allrecipes import AllrecipesHandler
from handlers.kingarthur import KingArthurHandler
from handlers.tasty import TastyHandler
from handlers.wordpress import WordpressHandler
from handlers.wordpress_tasty import WordpressTastyHandler


@dataclass
class Amount:
    field: int
    unit: str


@dataclass
class Recipe:
    active_time: int = 0
    yield_: [int, str] = 0

    ingredients: List[Tuple[Amount, str]] = field(default_factory=list)

    instructions: List[str] = field(default_factory=list)

    notes: List[str] = field(default_factory=list)


handlers = [SeriousEatsHandler,
            AllrecipesHandler,
            KingArthurHandler,
            TastyHandler,
            WordpressHandler,
            WordpressTastyHandler
            ]


def url_to_recipe(url: str) -> Recipe:

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:88.0) Gecko/20100101 Firefox/88.0"
    }
    req = r.get(url, headers=headers)
    if req.status_code != 200:
        print(f"Error {req.status_code}")
        raise Exception

    raw_html = req.text
    soup = BeautifulSoup(raw_html, "html.parser")

    handler = None
    handler_found = False
    for h in handlers:
        handler = h()
        try:
            if handler.instructions(soup) and handler.ingredients(soup):
                handler_found = True
                break
        except:
            pass

    if not handler_found:
        raise Exception("No usable handler found.")

    recipe = Recipe()

    recipe.title = h().title(soup)
    recipe.author = h().author(soup)
    recipe.source = h().source(soup)
    recipe.ingredients = h().ingredients(soup)
    recipe.instructions = h().instructions(soup)
    recipe.yield_ = h().yield_(soup)
    recipe.notes = h().notes(soup)
    recipe.time = h().time(soup)

    return recipe


if __name__ == "__main__":
    recipe = url_to_recipe(argv[1])

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
