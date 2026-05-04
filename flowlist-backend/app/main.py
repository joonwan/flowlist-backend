from fastapi import FastAPI, HTTPException
from app.schemas.task import Task, TaskCreate

app = FastAPI()

tasks: list[Task] = []

@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}

# task 전체 조회
@app.get("/tasks")
def get_tasks():
    return tasks

# new task 등록
@app.post("/tasks")
def create_task(task_data: TaskCreate):
    new_task = Task(
        id = len(tasks) + 1,
        title = task_data.title,
        is_done = False
    )

    tasks.append(new_task)
    return new_task

# task 단건 조회 
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Task not found")

# task 수정
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskCreate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = Task(
                id = task.id,
                title=task_data.title,
                is_done=task.is_done
            )
            tasks[index] = updated_task
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found")

# task 삭제
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)
    raise HTTPException(status_code=404, detail="Task not found")