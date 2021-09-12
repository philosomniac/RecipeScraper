"""It's a recipe"""

from __future__ import annotations

import json

from models.ingredient_set import IngredientSet
from models.instruction_set import InstructionSet

from pydantic import BaseModel


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
        return Recipe._json_to_recipe(recipe_json)

    @staticmethod
    def _recipe_decode(json_to_decode: dict):
        if 'ingredient_set' in json_to_decode:
            ingredient_set = IngredientSet(
                ingredients=json_to_decode['ingredient_set']['ingredients'])
            del json_to_decode['ingredient_set']
            recipe = Recipe(ingredient_set=ingredient_set, **json_to_decode)
            return recipe

        return json_to_decode

    @staticmethod
    def _json_to_recipe(recipe_json: str):
        recipe = json.loads(recipe_json, object_hook=Recipe._recipe_decode)
        return recipe
