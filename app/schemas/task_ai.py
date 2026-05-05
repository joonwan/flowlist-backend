from pydantic import BaseModel

class TaskBreakdownResponse(BaseModel):
    subtasks: list[str]

