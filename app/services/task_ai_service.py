import json

from fastapi import HTTPException
from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from app.repositories.task_repository import get_task_record_by_id
from app.schemas.task_ai import TaskBreakdownResponse

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)


def breakdown_task(db: Session, task_id: int) -> TaskBreakdownResponse:
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    messages = [
        {
            "role": "developer",
            "content": (
                "You are a task planning assistant. "
                "Break the given task into 3 to 5 short actionable subtasks. "
                "Each subtask must be a short sentence. "
                'Respond with only one JSON object in this exact format: {"subtasks": ["subtask 1", "subtask 2"]}.'
            ),
        },
        {
            "role": "user",
            "content": (
                "title: Learn SQLAlchemy basics\n"
                "description: Understand models, sessions, and CRUD operations\n"
                "priority: 2\n"
                "due_date: 2026-05-10"
            ),
        },
        {
            "role": "assistant",
            "content": (
                '{"subtasks": ['
                '"Read how SQLAlchemy models are defined", '
                '"Create a simple model with mapped columns", '
                '"Practice creating and querying records", '
                '"Update and delete records with a session"'
                "]}"
            ),
        },
        {
            "role": "user",
            "content": (
                "title: Add Redis cache to FastAPI\n"
                "description: Cache task list responses and invalidate cache after updates\n"
                "priority: 2\n"
                "due_date: 2026-05-11"
            ),
        },
        {
            "role": "assistant",
            "content": (
                '{"subtasks": ['
                '"Install and connect a Redis client", '
                '"Cache the task list response", '
                '"Set a TTL for cached data", '
                '"Delete cache after create update and delete"'
                "]}"
            ),
        },
        {
            "role": "user",
            "content": (
                f"title: {task.title}\n"
                f"description: {task.description}\n"
                f"priority: {task.priority}\n"
                f"due_date: {task.due_date}"
            ),
        },
    ]

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL, messages=messages, temperature=0.3
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to call llm")

    content = response.choices[0].message.content
    print(content)
    if not content:
        raise HTTPException(status_code=500, detail="llm returned empty response")

    try:
        parsed = json.loads(content) # json to dict
        return TaskBreakdownResponse(**parsed)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="llm returned invalid json")
