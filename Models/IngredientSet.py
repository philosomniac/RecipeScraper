class IngredientSet:
    def __init__(self, ingredient_list):
        self.ingredients = ingredient_list
        pass

    def __eq__(self, other: object) -> bool:
        return self.ingredients == other
