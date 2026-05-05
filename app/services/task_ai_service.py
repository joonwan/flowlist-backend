import json

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.task_repository import get_task_record_by_id
from app.schemas.task_ai import TaskBreakdownResponse

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:3b"


def breakdown_task(db: Session, task_id: int) -> TaskBreakdownResponse:
    task = get_task_record_by_id(db, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    prompt = f"""
                You are a task planning assistant.

                Break the following task into short, actionable subtasks.
                Return only valid JSON in this format:
                {{"subtasks": ["step 1", "step 2", "step 3"]}}

                Task title: {task.title}
                Task description: {task.description}
                Priority: {task.priority}
                Due date: {task.due_date}
            """.strip()

    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
        },
        timeout=60.0,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to call Ollama")

    result = response.json()
    content = result.get("response", "").strip()

    try:
        parsed = json.loads(content)
        return TaskBreakdownResponse(**parsed)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Ollama returned invalid JSON")
