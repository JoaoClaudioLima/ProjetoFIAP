from datetime import datetime
from typing import Union

from faker import Faker
from sqlalchemy.orm import Session

from src.model.database import User
from src.model.user_schemas import UserInput, UserUpdateInput, UserAuthentication
from src.utils.miscelaneous import hash_password
from src.utils.task import db_remove_user_from_tasks


def db_generate_fake_user():
    fake = Faker()
    name = fake.name()
    first_name = name.split()[0].lower()
    last_name = name.split()[1].lower()
    username = f"{first_name[0]}.{last_name}"
    email = f"{first_name}.{last_name}@fakemail.com"
    hashed_password = hash_password(fake.password())

    return username, email, name, hashed_password


def db_read_user(
        db: Session,
        user_id: Union[int, None] = None,
        skip: int = 0,
        limit: int = 10
    ):

    model = User

    if not user_id:
        return db.query(model).filter(model.deleted_at.is_(None)).offset(skip).limit(limit).all()

    return db.query(model).filter(model.id == user_id).all()


def db_login_user(user: UserAuthentication, db: Session):
    hashed_password = hash_password(user.password)
    return user.verify_password(hashed_password)


def db_create_user(user: UserInput, db: Session):

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def db_delete_user(db: Session, user: UserUpdateInput):
    model = User
    task = db.query(model).filter(model.email == user.to_update.email, model.deleted_at.is_(None)).first()
    if task:
        time = datetime.utcnow()
        task.updated_at, task.deleted_at = time, time
        db.commit()
        db.refresh(task)
        db_remove_user_from_tasks(db, str(task.id))

    return task


def db_update_user(db: Session, user: UserUpdateInput):
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

    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)

    return task
