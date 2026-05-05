from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


# find all Task
def get_all_task_records(db: Session):
    return db.query(Task).all()


# create Task
def create_task_record(db: Session, task_data: TaskCreate):
    new_task = Task(title=task_data.title, is_done=False)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# find single Task by primary key
def get_task_record_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


# update Task
def update_task_record(db: Session, task: Task, task_data: TaskUpdate):
    task.title = task_data.title
    task.is_done = task_data.is_done

    db.commit()
    db.refresh(task)
    return task


# delete Task
def delete_task_record(db: Session, task: Task):
    db.delete(task)
    db.commit()
