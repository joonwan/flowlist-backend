from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.repositories.task_repository import (
    get_all_task_records,
    get_task_record_by_id,
    create_task_record,
    update_task_record,
    delete_task_record,
)

from app.database import get_db
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks")


# task 전체 조회
@router.get("", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return get_all_task_records(db)


# new task 등록
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return create_task_record(db, task_data)


# task 단건 조회
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# task 수정
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return update_task_record(db, task, task_data)

# task 삭제
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    delete_task_record(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
