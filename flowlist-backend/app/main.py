from fastapi import FastAPI, HTTPException
from app.routers.tasks import router as tasks_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Flow List API is Running"}

app.include_router(tasks_router)