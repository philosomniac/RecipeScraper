# """The API that will retrieve the recipe data"""

# from fastapi import FastAPI
# from recipe_scraper.persistence_handler import PersistenceHandler


# app = FastAPI()


# @app.get("/")
# async def root():
#     """docstring"""
#     return {"message": "Hello World"}


# @app.get("/recipes/{name}")
# async def get_recipe_by_name(name):
#     persistence = PersistenceHandler()
#     return persistence.get_recipe_by_name(name).dict()
