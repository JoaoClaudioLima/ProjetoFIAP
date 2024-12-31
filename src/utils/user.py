from datetime import datetime
from typing import Union

from faker import Faker
from sqlalchemy.orm import Session

from src.model.database import User
from src.model.user_schemas import UserInput, UserUpdateInput
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
    if not task:
        return

    if new_password := user.to_update.password:
        task.hashed_password = hash_password(new_password)

    if new_full_name := user.to_update.full_name:
        task.full_name = new_full_name

    if new_username := user.to_update.username:
        task.username = new_username

    if not any([new_password, new_full_name, new_username]):
        return

    db.commit()
    db.refresh(task)

    return task
