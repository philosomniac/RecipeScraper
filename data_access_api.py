from fastapi import FastAPI
from persistence_handler import PersistenceHandler

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
