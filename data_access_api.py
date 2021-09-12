"""The API that will retrieve the recipe data"""

from fastapi import FastAPI
# from persistence_handler import PersistenceHandler


app = FastAPI()


@app.get("/")
async def root():
    """docstring"""
    return {"message": "Hello World"}
