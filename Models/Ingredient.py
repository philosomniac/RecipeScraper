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
