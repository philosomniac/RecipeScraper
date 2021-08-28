import json


class Ingredient:
    def __init__(self, name: str, amount: str, unit: str, price: float):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.price = price
        pass

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ingredient):
            return self.name == other.name
        return False

    @classmethod
    def from_json(cls, ingredient_json: str):
        parsed = json.loads(ingredient_json)
        ingredient = cls(**parsed)
        return ingredient
