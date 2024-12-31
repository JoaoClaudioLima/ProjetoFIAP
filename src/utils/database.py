from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.controller.database import SessionLocal
from src.model.database import User
from src.utils.miscelaneous import verify_password


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_email_exists(db: Session, email: str):
    model = User
    if db.query(model).filter(model.email == email, model.deleted_at.is_(None)).first():
        return True
    return False


def get_from_db(model, db: Session, skip: int = 0, limit: int = 10):
    return db.query(model).offset(skip).all()


def is_user_admin(db: Session, email: str):
    model = User
    task = db.query(model).filter(model.email == email, model.deleted_at.is_(None), model.is_admin.is_(True)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Only admins can perform this action")
    return task


def check_email(authenticate_email: str, to_update_email: str) -> bool:
    return authenticate_email == to_update_email


def can_user_update(db: Session, authenticate_email: str, to_update_email: str) -> bool:
    return any([is_user_admin(db, authenticate_email), check_email(authenticate_email, to_update_email)])


def check_password(password, hashed_password) -> bool:
    return verify_password(plain_password=password, hashed_password=hashed_password)


def check_authentication(db: Session, email: str, password: str) -> bool:
    model = User
    task = db.query(model).filter(model.email == email, model.deleted_at.is_(None)).first()
    return check_password(password, task.hashed_password)


def validate_username_availability(username: str):
    model = User
    db: Session = SessionLocal()
    try:
        if db.query(model).filter(model.username == username, model.deleted_at.is_(None)).first():
            raise HTTPException(status_code=400, detail="Username already taken")
    finally:
        db.close()


def validate_email_availability(email: str):
    model = User
    db: Session = SessionLocal()
    try:
        if db.query(model).filter(model.email == email, model.deleted_at.is_(None)).first():
            raise HTTPException(status_code=400, detail="Email already taken")
    finally:
        db.close()


def authenticate_user(db: Session, authentication_email: str, to_update_email: str, password: str):
    if not check_authentication(db, email=authentication_email, password=password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not can_user_update(db, authenticate_email=authentication_email, to_update_email=to_update_email):
        raise HTTPException(status_code=400, detail="User can only update their profile")
