from Models.Recipe import Recipe


class PersistenceHandler():

    def __init__(self):
        self._persistence_file = 'recipedb.txt'

    def get_recipe_by_url(self, url) -> Recipe:
        with open(self._persistence_file, "r") as persistence_store:
            for recipe_str in persistence_store:
                recipe = Recipe.from_json(recipe_str)
                if recipe.url == url:
                    return recipe
        return None

    def save_recipe_to_persistence(self, recipe: Recipe):
        pre_existing_recipe = self.get_recipe_by_url(recipe.url)

        if pre_existing_recipe is None:
            with open(self._persistence_file, "a+") as persistence_store:
                persistence_store.write(recipe.to_json() + "\n")
        else:
            self._delete_recipe_from_persistence(recipe.url)
            with open(self._persistence_file, "a") as persistence_store:
                persistence_store.write(recipe.to_json() + "\n")

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
            return matchingRecipesCount

    def _delete_recipe_from_persistence(self, url: str):
        with open(self._persistence_file, "r+") as persistence_store:
            recipe_list = map(Recipe.from_json, persistence_store.readlines())
            persistence_store.seek(0)
            for recipe in recipe_list:
                if recipe.url != url:
                    persistence_store.write(recipe.to_json() + "\n")
                pass
            persistence_store.truncate()


class RecipeNotFoundException(Exception):
    pass


class RecipeAlreadyExistsException(Exception):
    pass
