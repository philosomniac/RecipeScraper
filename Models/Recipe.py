from __future__ import annotations
from Models.IngredientSet import IngredientSet
import json


class Recipe:
    def __init__(self, url="", name=None, ingredient_set: IngredientSet = IngredientSet([]), total_cost=None, serving_cost=None, servings=None, prep_time=None, cook_time=None, instruction_set=None, img_url=None):
        self.url = url
        self.name = name
        self.ingredient_set = ingredient_set
        self.total_cost = total_cost
        self.serving_cost = serving_cost
        self.servings = servings
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.instruction_set = instruction_set
        self.img_url = img_url
        pass

    def __eq__(self, o: Recipe) -> bool:
        return self.url == o.url and \
            self.name == o.name and \
            self.img_url == self.img_url and \
            self.ingredient_set == o.ingredient_set and \
            self.instruction_set == self.instruction_set

    def to_json(self) -> str:
        return json.dumps(self, default=lambda x: vars(x))

    @classmethod
    def from_json(cls, recipe_json: str) -> Recipe:
        return Recipe._json_to_recipe(recipe_json)

    @staticmethod
    def _recipe_decode(json_to_decode: dict):
        if 'ingredient_set' in json_to_decode:
            myIngredientSet = IngredientSet(
                json_to_decode['ingredient_set']['ingredients'])
            del json_to_decode['ingredient_set']
            myRecipe = Recipe(ingredient_set=myIngredientSet, **json_to_decode)
            return myRecipe

        return json_to_decode

    @staticmethod
    def _json_to_recipe(recipe_json: str):
        recipe = json.loads(recipe_json, object_hook=Recipe._recipe_decode)
        return recipe
