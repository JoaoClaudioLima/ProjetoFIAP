from datetime import datetime
from typing import Union

from faker import Faker
from sqlalchemy.orm import Session

from src.model.database import User
from src.model.schemas import UserInput, UserUpdateInput
from src.utils.miscelaneous import hash_password


def generate_fake_user():
    fake = Faker()
    name = fake.name()
    first_name = name.split()[0].lower()
    last_name = name.split()[1].lower()
    username = f"{first_name[0]}.{last_name}"
    email = f"{first_name}.{last_name}@fakemail.com"
    hashed_password = hash_password(fake.password())

    return username, email, name, hashed_password


def get_db_user(
        db: Session,
        user_id: Union[int, None] = None,
        skip: int = 0,
        limit: int = 10
    ):

    model = User

    if not user_id:
        return db.query(model).filter(model.deleted_at.is_(None)).offset(skip).limit(limit).all()

    return db.query(model).filter(model.id == user_id).all()


def create_new_db_user(user: UserInput, db: Session):

    hashed_password = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,  # TODO Validar se será criptografado na camada de back ou front. Estou fazendo aqui no momento.
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_db_user(db: Session, user: UserUpdateInput):
    model = User
    task = db.query(model).filter(model.email == user.to_update.email,model.deleted_at.is_(None)).first()
    if task:
        task.deleted_at = datetime.now()
        db.commit()
        db.refresh(task)
    return task


def update_db_user(db: Session, user: UserUpdateInput):
    model = User
    task = db.query(model).filter(model.email == user.to_update.email, model.deleted_at.is_(None)).first()
    if task:
        task.password = hash_password(user.to_update.password) if user.to_update.password else task.password
        task.full_name = user.full_name if user.full_name else task.full_name
        task.username = user.username if user.username else task.username
        db.commit()
        db.refresh(task)
    return task
