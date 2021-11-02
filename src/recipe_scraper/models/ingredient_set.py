from __future__ import annotations
from recipe_scraper.models.ingredient import Ingredient
from pydantic import BaseModel

from typing import List


class IngredientSet(BaseModel):

    ingredients: List[Ingredient]

    def __eq__(self, other: object) -> bool:
        return self.ingredients == other
