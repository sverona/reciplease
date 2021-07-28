from dataclasses import dataclass, field
from re import sub
from sys import argv

from bs4 import BeautifulSoup
import requests as r

from typing import List, Tuple


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


def url_to_recipe(url: str) -> Recipe:
    req = r.get(url)
    if req.status_code != 200:
        raise Exception

    raw_html = req.text
    soup = BeautifulSoup(raw_html, "html.parser")

    recipe = Recipe()

    ingredients_section = soup.find("section", class_="section--ingredients")
    ingredients = ingredients_section.select("ul li")

    recipe.ingredients = [li.text.strip() for li in ingredients]

    # TODO Make a website to ID dict
    instructions_section = soup.find("section", class_="section--instructions")

    instructions = instructions_section.select("ol li")
    # instructions = [tag for li in instructions for tag in li.find_all(lambda tag: tag.name != "figure")]

    recipe.instructions = [sub(r"\n[\n\t ]+", r"\n", li.text).strip() for li in instructions]

    return recipe


recipe = url_to_recipe(argv[1])

print(recipe)
