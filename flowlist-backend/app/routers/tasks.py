from fastapi import APIRouter, HTTPException
from app.schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks")

tasks: list[Task] = []

# task 전체 조회
@router.get("", response_model=list[Task])
def get_tasks():
    return tasks


# new task 등록
@router.post("", response_model=list[Task])
def create_task(task_data: TaskCreate):
    new_task = Task(id=len(tasks) + 1, title=task_data.title, is_done=False)

    tasks.append(new_task)
    return new_task


# task 단건 조회
@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


# task 수정
@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = Task(
                id=task.id, title=task_data.title, is_done=task_data.is_done
            )
            tasks[index] = updated_task
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found")


# task 삭제
@router.delete("/{task_id}", response_model=Task)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(index)
    raise HTTPException(status_code=404, detail="Task not found")