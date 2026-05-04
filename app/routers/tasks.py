from fastapi import APIRouter, HTTPException, Response, status
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks")

tasks: list[TaskResponse] = []


# task 전체 조회
@router.get("", response_model=list[TaskResponse])
def get_tasks():
    return tasks


# new task 등록
@router.post("", response_model=list[TaskResponse], status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    new_task = TaskResponse(id=len(tasks) + 1, title=task_data.title, is_done=False)

    tasks.append(new_task)
    return new_task


# task 단건 조회
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


# task 수정
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task = TaskResponse(
                id=task.id, title=task_data.title, is_done=task_data.is_done
            )
            tasks[index] = updated_task
            return tasks[index]
    raise HTTPException(status_code=404, detail="Task not found")


# task 삭제
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(index)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Task not found")
