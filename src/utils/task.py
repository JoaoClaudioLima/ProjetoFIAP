from random import randint
from typing import Union

from faker import Faker
from sqlalchemy.orm import Session

from src.model.database import Task


def generate_fake_task(iteration, users_ammount: int = 5, status_ammount: int = 3):
    fake = Faker()
    name = f"Tarefa {iteration + 1}"
    description = fake.sentence()
    status_id = randint(1, status_ammount)
    user_id = randint(1, users_ammount)
    return name, description, status_id, user_id


def get_task_from_db(
        db: Session,
        user_id: Union[int, None],
        task_id: Union[int, None],
        status_id: Union[int, None],
        skip: int = 0,
        limit: int = 10
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
