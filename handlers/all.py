"""Exposes a variable containing all possible `RecipeHandler`s.

The order of the array matters because running a handler is expensive.
Wordpress handlers up front because they comprise probably 50% of recipes.
Remaining handlers listed in alphabetical order.
"""

from .allrecipes import AllrecipesHandler
from .bbc import BBCHandler
from .delish import DelishHandler
from .epicurious import EpicuriousHandler
from .food52 import Food52Handler
from .kingarthur import KingArthurHandler
from .seriouseats import SeriousEatsHandler
from .tasty import TastyHandler
from .wordpress import WordpressHandler
from .wordpress_tasty import (
    WordpressTastyV3Handler,
    WordpressTastyPreV3Handler,
)

ALL_HANDLERS = [
    WordpressHandler,
    WordpressTastyV3Handler,
    WordpressTastyPreV3Handler,
    AllrecipesHandler,
    BBCHandler,
    DelishHandler,
    EpicuriousHandler,
    Food52Handler,
    KingArthurHandler,
    SeriousEatsHandler,
    TastyHandler,
]
