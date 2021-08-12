class Recipe:
    def __init__(self, url="", name=None, ingredient_set=None, total_cost=None, serving_cost=None, servings=None, prep_time=None, cook_time=None, instruction_set=None, img_url=None):
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
