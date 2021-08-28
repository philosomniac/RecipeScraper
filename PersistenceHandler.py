from Models.Recipe import Recipe


class PersistenceHandler():

    def __init__(self):
        self._persistence_file = 'recipedb.txt'

    def get_recipe(self) -> Recipe:
        return Recipe()

    def save_recipe_to_persistence(self, recipe: Recipe):
        with open(self._persistence_file, "a+") as persistence_store:
            persistence_store.write(recipe.to_json() + "\n")

    def save_recipes_to_persistence(self, recipe_list: list[Recipe]):
        with open(self._persistence_file, "a+") as persistence_store:
            for recipe in recipe_list:
                persistence_store.write(recipe.to_json() + "\n")
