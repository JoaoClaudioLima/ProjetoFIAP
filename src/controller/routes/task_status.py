from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from src.model.database import TaskStatus
from src.utils.database import get_from_db, get_db

task_status_router = APIRouter()


@task_status_router.get("/task-status/", response_model=None)
def read_task_status(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    task_status = get_from_db(TaskStatus, db, skip=skip, limit=limit)
    return task_status
