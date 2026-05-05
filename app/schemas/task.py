from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=255)]
    description: str | None = None
    priority: Annotated[int, Field(ge=1, le=3)] = 1
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=255)]
    description: str | None = None
    priority: Annotated[int, Field(ge=1, le=3)] = 1
    due_date: date | None = None
    is_done: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: int
    due_date: date | None
    is_done: bool
