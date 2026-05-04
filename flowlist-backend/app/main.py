from fastapi import FastAPI
from app.schemas.task import Task, TaskCreate

app = FastAPI()

tasks: list[Task] = []

@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post("/tasks")
def create_task(task_data: TaskCreate):
    new_task = Task(
        id = len(tasks) + 1,
        title = task_data.title,
        is_done = False
    )

    tasks.append(new_task)
    return new_task