from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db

from app.services import task_service, task_ai_service

from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from app.schemas.task_ai import TaskBreakdownResponse

router = APIRouter(prefix="/tasks")


# task 전체 조회
@router.get("", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)


# new task 등록
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task_data)


# task 단건 조회
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)


# task 수정
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    return task_service.update_task(db, task_id, task_data)


# task 삭제
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ai 기반 task 쪼개는 endpoint
@router.post("/{task_id}/breakdown", response_model=TaskBreakdownResponse)
def breakdown_task(task_id: int, db: Session = Depends(get_db)):
    return task_ai_service.breakdown_task(db, task_id)