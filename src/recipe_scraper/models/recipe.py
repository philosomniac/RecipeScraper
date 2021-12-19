"""It's a recipe"""

from __future__ import annotations

import json

from pydantic import BaseModel
from models.ingredient_set import IngredientSet


class Recipe(BaseModel):
    """Represents a recipe"""

    url: str
    name: str
    ingredient_set: IngredientSet
    total_cost: float = 0
    serving_cost: float = 0
    servings: int = 1
    prep_time: int = 0
    cook_time: int = 0
    # instruction_set: InstructionSet
    img_url: str = ""

    @classmethod
    def from_json(cls, recipe_json: str) -> Recipe:
        """Constructs a recipe from its JSON respresentation"""
        # return Recipe._json_to_recipe(recipe_json)
        return Recipe.parse_raw(recipe_json)
