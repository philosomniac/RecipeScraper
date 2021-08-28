from Models.Ingredient import Ingredient


class IngredientSet:
    def __init__(self, ingredient_list: list):
        self.ingredients = []
        for list_item in ingredient_list:
            if isinstance(list_item, Ingredient):
                self.ingredients.append(list_item)
            elif isinstance(list_item, str):
                self.ingredients.append(Ingredient.from_json(list_item))
            elif isinstance(list_item, dict):
                self.ingredients.append(Ingredient(**list_item))

        pass

    def __eq__(self, other: object) -> bool:
        return self.ingredients == other

    # def __dict__(self):
    #     return [x.__dict__ for x in self.ingredients]
