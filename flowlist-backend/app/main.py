from fastapi import FastAPI
from app.schemas.task import Task, TaskCreate

app = FastAPI()

tasks: list[Task] = []

@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}

@app.get("/tasks")
def get_taks():
    return tasks