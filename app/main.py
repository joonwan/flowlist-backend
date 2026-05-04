from fastapi import FastAPI, HTTPException
from app.routers.tasks import router as tasks_router
from app.models.task import Task
from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}


app.include_router(tasks_router)
