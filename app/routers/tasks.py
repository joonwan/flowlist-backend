from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks")


# task 전체 조회
@router.get("", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


# new task 등록
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title = task_data.title,
        is_done=False,
    )
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
    

# task 단건 조회
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
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
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if task is None:    
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.title = task_data.title
    task.is_done = task_data.is_done
    
    db.commit()
    db.refresh(task)
    return task


# task 삭제
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
