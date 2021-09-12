from models.ingredient import Ingredient
from pydantic import BaseModel


class IngredientSet(BaseModel):

    ingredients: list[Ingredient]

    # def __init__(self, ingredient_list: list[Ingredient]):
    #     # self.ingredients = []
    #     for list_item in ingredient_list:
    #         if isinstance(list_item, Ingredient):
    #             self.ingredients.append(list_item)
    #         elif isinstance(list_item, str):
    #             self.ingredients.append(Ingredient.from_json(list_item))
    #         elif isinstance(list_item, dict):
    #             self.ingredients.append(Ingredient(**list_item))

    def __eq__(self, other: object) -> bool:
        return self.ingredients == other
