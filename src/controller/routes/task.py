from typing import Optional

from fastapi import Depends, Query, APIRouter
from sqlalchemy.orm import Session

from src.model.database import Task
from src.utils.database import get_from_db, get_db
from src.utils.task import get_task_from_db

task_router = APIRouter()


@task_router.get("/task/", response_model=None)
def read_tasks(
        user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"),
        status_id: Optional[int] = Query(None, description="The ID of the status to retrieve"),
        task_id: Optional[int] = Query(None, description="The ID of the task to retrieve"),
        skip: int = 0,
        db: Session = Depends(get_db)
    ):
    query_params = [user_id, status_id, task_id]

    if any([user_id, status_id, task_id]):
        task = get_task_from_db(db=db, user_id=user_id, status_id=status_id, task_id=task_id)
        return task

    tasks = get_from_db(Task, db, skip=skip)
    return tasks
