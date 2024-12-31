from typing import Optional

from fastapi import Depends, Query, APIRouter
from sqlalchemy.orm import Session

from src.model.database import Tasks
from src.model.task_schemas import TaskInput
from src.utils.database import get_from_db, get_db
from src.utils.task import get_task_from_db

tasks_router = APIRouter()


@tasks_router.get("/tasks/", response_model=None)
def read_tasks(
        user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"),
        status_id: Optional[int] = Query(None, description="The ID of the status to retrieve"),
        task_id: Optional[int] = Query(None, description="The ID of the task to retrieve"),
        skip: int = 0,
        db: Session = Depends(get_db)
    ):

    if any([user_id, status_id, task_id]):
        task = get_task_from_db(db=db, user_id=user_id, status_id=status_id, task_id=task_id)
        return task

    tasks = get_task_from_db(db=db, skip=skip)
    return tasks


@tasks_router.post("/tasks/", response_model=None, status_code=201)
def create_user(user: TaskInput, db: Session = Depends(get_db)):
    # create_new_db_task(user, db)
    return "Created"
