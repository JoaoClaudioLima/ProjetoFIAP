from datetime import datetime
from fastapi import HTTPException
from random import randint
from typing import Union

from faker import Faker
from sqlalchemy.orm import Session

from src.model.database import Task
from src.model.task_schemas import TaskInput, TaskUpdateInput
from src.utils.database import check_user_exists, check_task_status_exists


def db_create_fake_task(iteration, users_ammount: int = 5, status_ammount: int = 3):
    fake = Faker()
    name = f"Tarefa {iteration + 1}"
    description = fake.sentence()
    status_id = randint(1, status_ammount)
    user_id = randint(1, users_ammount)
    return name, description, status_id, user_id


def db_read_task(
        db: Session,
        user_id: Union[int, None] = None,
        task_id: Union[int, None] = None,
        status_id: Union[int, None] = None,
    ):
    model = Task
    query = db.query(Task)

    if user_id is not None:
        query = query.filter(model.user_id == user_id)
    if status_id is not None:
        query = query.filter(model.status_id == status_id)
    if task_id is not None:
        query = query.filter(model.id == task_id)

    query = query.filter(model.deleted_at.is_(None))

    return query.all()


def db_validate_task_input(task_input: Union[TaskInput, TaskUpdateInput], db: Session):
    if task_input.user_id and not check_user_exists(db, str(task_input.user_id)):
        raise HTTPException(status_code=400, detail="Usuário não encontrado.")

    if task_input.status_id and not check_task_status_exists(db, str(task_input.status_id)):
        raise HTTPException(status_code=400, detail="Status da tarefa inválido.")


def db_create_task(task_input: TaskInput, db: Session):

    db_validate_task_input(task_input, db)

    task = Task(
        title=task_input.title,
        description=task_input.description,
        status_id=task_input.status_id if task_input.status_id else 1,
        user_id=task_input.user_id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def db_delete_task(db: Session, task_id: int):
    model = Task
    task = db.query(model).filter(model.id == task_id, model.deleted_at.is_(None)).first()
    if task:
        time = datetime.utcnow()
        task.updated_at, task.deleted_at = time, time
        db.commit()
        db.refresh(task)
    return task


def db_update_task(db: Session, task_input: TaskUpdateInput, task_id: str, remove_user: bool):

    db_validate_task_input(task_input, db)

    model = Task
    task = db.query(model).filter(model.id == task_id, model.deleted_at.is_(None)).first()
    if not task:
        return

    if remove_user:
        task.user_id = None
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)

        return task

    if new_title := task_input.title:
        task.title = new_title

    if new_description := task_input.description:
        task.description = new_description

    if new_status_id := task_input.status_id:
        task.status_id = new_status_id

    if new_user_id := task_input.user_id:
        task.user_id = new_user_id

    if not any([new_title, new_description, new_status_id, new_user_id]):
        return

    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return task


def db_remove_user_from_tasks(db: Session, user_id: str):
    model = Task
    tasks = db.query(model).filter(model.user_id == user_id, model.deleted_at.is_(None)).all()
    for task in tasks:
        task.user_id = None
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
