import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.redis_client import redis_client
from app.repositories.task_repository import (
    create_task_record,
    update_task_record,
    delete_task_record,
    get_all_task_records,
    get_task_record_by_id,
)
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

TASKS_ALL_CACHE_KEY = "tasks:all"


def get_tasks(db: Session):
    cached_tasks = redis_client.get(TASKS_ALL_CACHE_KEY)

    if cached_tasks:
        return json.loads(cached_tasks)

    tasks = get_all_task_records(db)

    serialized_tasks = [
        TaskResponse.model_validate(task).model_dump(mode="json")
        for task in tasks
    ]
    redis_client.set(TASKS_ALL_CACHE_KEY, json.dumps(serialized_tasks), ex=60)

    return tasks


def get_task(db: Session, task_id: int):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, task_data: TaskCreate):
    task = create_task_record(db, task_data)
    redis_client.delete(TASKS_ALL_CACHE_KEY)
    return task


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task = update_task_record(db, task, task_data)
    redis_client.delete(TASKS_ALL_CACHE_KEY)
    return updated_task


def delete_task(db: Session, task_id: int):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task_record(db, task)
    redis_client.delete(TASKS_ALL_CACHE_KEY)
