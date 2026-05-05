from pydantic import BaseModel
from datetime import date


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: int = 1
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    priority: int = 1
    due_date: date | None = None
    is_done: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    due_date: date | None
    is_done: bool
