from __future__ import annotations

import json
from typing import List

from pydantic import BaseModel


class Costs():
    def __init__(self, serving_cost=None, recipe_cost=None):
        self.serving_cost = serving_cost
        self.recipe_cost = recipe_cost


class Ingredient(BaseModel):

    name: str
    amount: str
    unit: str
    price: float

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ingredient):
            return self.name == other.name
        return False

    @classmethod
    def from_json(cls, ingredient_json: str):
        parsed = json.loads(ingredient_json)
        ingredient = cls(**parsed)
        return ingredient


class IngredientSet(BaseModel):

    ingredients: List[Ingredient]

    def __eq__(self, other: object) -> bool:
        return self.ingredients == other


class InstructionSet:
    # TODO: implement instruction set model
    pass


class InstructionStep:
    def __init__(self):
        pass


class MeasurementUnit:
    def __init__(self, name):
        pass


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

    @ classmethod
    def from_json(cls, recipe_json: str) -> Recipe:
        """Constructs a recipe from its JSON respresentation"""
        # return Recipe._json_to_recipe(recipe_json)
        return Recipe.parse_raw(recipe_json)
