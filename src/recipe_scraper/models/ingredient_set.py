from recipe_scraper.models.ingredient import Ingredient
from pydantic import BaseModel


class IngredientSet(BaseModel):

    ingredients: list[Ingredient]

    def __eq__(self, other: object) -> bool:
        return self.ingredients == other
