from fastapi import FastAPI
from app.schemas.task import Task, TaskCreate

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}