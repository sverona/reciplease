from sys import argv

from bs4 import BeautifulSoup
import requests as r

from handlers import Recipe
from handlers.all import ALL_HANDLERS


def get_soup(url: str) -> BeautifulSoup:
    """cURL the provided `url`.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:88.0)"
                      "Gecko/20100101 Firefox/88.0"
    }
    resp = r.get(url, headers=headers)
    resp.raise_for_status()

    raw_html = resp.text
    return BeautifulSoup(raw_html, "html.parser")


def from_url(url: str) -> Recipe:
    """Parse a recipe from a given URL.
    """
    soup = get_soup(url)
    for handler in ALL_HANDLERS:
        recipe = Recipe(soup, handler)
        if recipe.ingredients and recipe.instructions:
            return recipe
    raise Exception("No usable handler found.")


def main():
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
    main()
