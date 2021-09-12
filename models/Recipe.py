"""It's a recipe"""

from __future__ import annotations

import json

from models.ingredient_set import IngredientSet
from models.instruction_set import InstructionSet

from pydantic import BaseModel


class Recipe(BaseModel):
    """Represents a recipe"""

    # def __init__(
    #         self,
    #         url="",
    #         name=None,
    #         ingredient_set: IngredientSet = IngredientSet([]),
    #         total_cost=None,
    #         serving_cost=None,
    #         servings=None,
    #         prep_time=None,
    #         cook_time=None,
    #         instruction_set=None,
    #         img_url=None
    # ):
    #     self.url = url
    #     self.name = name
    #     self.ingredient_set = ingredient_set
    #     self.total_cost = total_cost
    #     self.serving_cost = serving_cost
    #     self.servings = servings
    #     self.prep_time = prep_time
    #     self.cook_time = cook_time
    #     self.instruction_set = instruction_set
    #     self.img_url = img_url

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

    # def __eq__(self, o: Recipe) -> bool:
    #     return self.url == o.url and \
    #         self.name == o.name and \
    #         self.img_url == self.img_url and \
    #         self.ingredient_set == o.ingredient_set and \
    #         self.instruction_set == self.instruction_set

    # def to_json(self) -> str:
    #     """Transforms a recipe into its JSON representation"""
    #     return json.dumps(self, default=lambda x: vars(x))

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
