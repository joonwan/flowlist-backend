from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.task_repository import (
    get_all_task_records,
    get_task_record_by_id,
    create_task_record,
    update_task_record,
    delete_task_record,
)

from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    return get_all_task_records(db)


def get_task(db: Session, task_id: int):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, task_data: TaskCreate):
    return create_task_record(db, task_data)


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return update_task_record(db, task, task_data)


def delete_task(db: Session, task_id: int):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task_record(db, task)
