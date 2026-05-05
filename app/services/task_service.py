import json
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.task_repository import (
    get_all_task_records,
    get_task_record_by_id,
    create_task_record,
    update_task_record,
    delete_task_record,
)

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.redis_client import redis_client

TASKS_ALL_CACHE_KEY = "tasks:all"

def get_tasks(db: Session):
    cached_tasks = redis_client.get(TASKS_ALL_CACHE_KEY)
    
    if cached_tasks:
        return json.loads(cached_tasks)
    
    tasks = get_all_task_records(db)
    
    """
    - db 에서 꺼낸 SQLAlchemy 객체를 redis 에 넣을 수 있는 json 형태로 바꾸는 과정
    - SQLAlchemy 객체는 그대로 json 직렬화가 안됨
    """
    serialized_tasks = [
        TaskResponse.model_validate(task).model_dump(mode="json") # SQLAlchemy Task 객체를 Pydantic 응답 스키마로 검증 및 변환하는 단계. 이후 pydantic model 을 json 으로 바꿀 수 있는 dict 형태로 변환
        for task in tasks
    ]
    redis_client.set(TASKS_ALL_CACHE_KEY, json.dumps(serialized_tasks), ex=60) # 60초 TTL 적용해 redis 에 캐싱
    
    return tasks


def get_task(db: Session, task_id: int):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def create_task(db: Session, task_data: TaskCreate):
    task =  create_task_record(db, task_data)
    redis_client.delete(TASKS_ALL_CACHE_KEY)
    return task;


def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updated_task =  update_task_record(db, task, task_data)
    redis_client.delete(TASKS_ALL_CACHE_KEY)
    return updated_task


def delete_task(db: Session, task_id: int):
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    delete_task_record(db, task)
    redis_client.delete(TASKS_ALL_CACHE_KEY)
