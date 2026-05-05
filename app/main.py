from fastapi import FastAPI

from app.infrastructure.database import Base, engine
from app.models.task import Task
from app.routers.tasks import router as tasks_router

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}


app.include_router(tasks_router)
