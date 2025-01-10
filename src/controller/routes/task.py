from typing import Optional

from fastapi import Depends, Query, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src.model.task_schemas import TaskInput, TaskUpdateInput
from src.utils.database import get_db
from src.utils.task import db_create_task, db_read_task, db_delete_task, db_update_task
from src.utils.user import db_update_user

tasks_router = APIRouter()


@tasks_router.get("/tasks/", response_model=None)
def read_tasks(
        user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"),
        status_id: Optional[int] = Query(None, description="The ID of the status to retrieve"),
        task_id: Optional[int] = Query(None, description="The ID of the task to retrieve"),
        db: Session = Depends(get_db)
):
    if any([user_id, status_id, task_id]):
        task = db_read_task(db=db, user_id=user_id, status_id=status_id, task_id=task_id)
        return task

    tasks = db_read_task(db=db)
    return tasks


@tasks_router.post("/tasks/", response_model=None, status_code=201)
def create_task(task: TaskInput, db: Session = Depends(get_db)):
    db_create_task(task, db)

    #  TODO validar erro de cadastro de status/user que não existem

    return "Tarefa criada"


@tasks_router.delete("/tasks/", response_model=None, status_code=200)
def delete_task(
        task_id: Optional[int] = Query(None, description="The ID of the task to be deleted"),
        db: Session = Depends(get_db)):
    task = db_delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=400, detail="Tarefa não encontrada")
    return "Tarefa deletada"


@tasks_router.put("/tasks/", response_model=None, status_code=200)
def update_task(
        task: TaskUpdateInput,
        task_id: Optional[str] = Query(None, description="The ID of the task to be updated"),
        remove_user: Optional[bool] = Query(False, description="Sets task user_id to None"),
        db: Session = Depends(get_db)):

    task = db_update_task(db=db, task_input=task, task_id=task_id, remove_user=remove_user)

    if not task:
        raise HTTPException(status_code=400, detail="Tarefa não pôde ser atualizada")
    return "Tarefa atualizada"
