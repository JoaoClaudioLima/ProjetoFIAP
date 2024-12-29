from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.controller.database import SessionLocal
from src.model import models
from src.settings import Settings

from src.utils.database import get_from_db, get_from_db_filter_id

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/health-check")
async def health_check():
    '''
    Check de saúde do serviço.
    '''
    data = {
        "version": Settings.VERSION,
        "message": "Alive and kicking!"
    }
    return data


@router.get("/")
async def home():
    data = {
        "message": "Hello World!"
    }
    return data


# CRUD for tasks table

@router.get("/tasks/", response_model=None)
def read_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = get_from_db(models.Task, db, skip=skip, limit=limit)
    return tasks


@router.get("/tasks/{task_id}", response_model=None)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_from_db_filter_id(models.Task, db, str(task_id))
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


# CRUD for task_status table

@router.get("/task-status/", response_model=None)
def read_task_status(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    task_status = get_from_db(models.TaskStatus, db, skip=skip, limit=limit)
    return task_status
