from Models.Recipe import Recipe


class PersistenceHandler():

    def __init__(self):
        self._persistence_file = 'recipedb.txt'

    def get_recipe(self) -> Recipe:
        with open(self._persistence_file, "r") as persistence_store:
            recipe_str = persistence_store.readline().strip()
            recipe = Recipe.from_json(recipe_str)
            return recipe

    def get_recipe_by_url(self, url) -> Recipe:
        with open(self._persistence_file, "r") as persistence_store:
            for recipe_str in persistence_store:
                recipe = Recipe.from_json(recipe_str)
                if recipe.url == url:
                    return recipe
        raise RecipeNotFoundException(f"Could not find recipe with url: {url}")

    def save_recipe_to_persistence(self, recipe: Recipe):
        with open(self._persistence_file, "a+") as persistence_store:
            pre_existing_recipe = self.get_recipe_by_url(recipe.url)
            if pre_existing_recipe is None:
                persistence_store.write(recipe.to_json() + "\n")
            else:
                pass

    def save_recipes_to_persistence(self, recipe_list: list[Recipe]):
        with open(self._persistence_file, "a+") as persistence_store:
            for recipe in recipe_list:
                persistence_store.write(recipe.to_json() + "\n")

    def count_recipes_with_url(self, url: str) -> int:
        with open(self._persistence_file, "r") as persistence_store:
            matchingRecipesCount = 0
            for recipe_str in persistence_store:
                recipe = Recipe.from_json(recipe_str)
                if recipe.url == url:
                    matchingRecipesCount += 1
            return


class RecipeNotFoundException(Exception):
    pass


class RecipeAlreadyExistsException(Exception):
    pass
