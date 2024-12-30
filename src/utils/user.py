from typing import Union

from faker import Faker
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model import models
from src.model.models import UserInput
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


def get_user_from_db(
        db: Session,
        user_id: Union[int, None] = None,
        email: Union[str, None] = None,
        username: Union[str, None] = None,
        skip: int = 0,
        limit: int = 10
    ):

    model = models.User

    if email and username:
        if db.query(model).filter(model.email == email and model.deleted_at.is_(None)).all():
            return True, "Email already registered"
        elif db.query(model).filter(model.username == username and model.deleted_at.is_(None)).all():
            return True, "Username already registered"
        return False, "OK"

    if not user_id:
        return db.query(model).filter(model.deleted_at.is_(None)).offset(skip).limit(limit).all(), "User not found"

    return db.query(model).filter(model.id == user_id).all(), None


def validate_user_input(user: UserInput, db: Session):
    db_user, message = get_user_from_db(db, email=user.email, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail=message)


def create_new_user(user: UserInput, db: Session):

    hashed_password = hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,  # TODO Validar se será criptografado na camada de back ou front. Estou fazendo aqui no momento.
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user():

    pass
