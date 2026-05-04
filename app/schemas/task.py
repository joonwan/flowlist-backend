from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str


class TaskResponse(BaseModel):
    id: int
    title: str
    is_done: bool


class TaskUpdate(BaseModel):
    title: str
    is_done: bool
