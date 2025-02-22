from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.controller.database import SessionLocal
from src.model.database import User, TaskStatus
from src.utils.miscelaneous import verify_password

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_email_exists(db: Session, email: str):
    model = User
    return db.query(model).filter(model.email == email, model.deleted_at.is_(None)).first() is not None


def check_user_exists(db: Session, user_id: str):
    model = User
    return db.query(model).filter(model.id == user_id, model.deleted_at.is_(None)).first() is not None


def check_task_status_exists(db: Session, task_status_id: str):
    model = TaskStatus
    return db.query(model).filter(model.id == task_status_id).first() is not None


def check_username_availability(db: Session, username: str):
    model = User
    task = db.query(model).filter(model.username == username).first()
    if task is not None:
        raise HTTPException(400, "Nome de usuário já existe.")


def get_from_db(model, db: Session, skip: int = 0):
    return db.query(model).offset(skip).all()


def get_user_from_db(db: Session, email: str):
    model = User
    task = db.query(model).filter(model.email == email).first()
    if not task:
        raise HTTPException(400, "Usuário não encontrado.")
    return task.id


def is_user_admin(db: Session, email: str):
    model = User
    return db.query(model).filter(model.email == email, model.deleted_at.is_(None), model.is_admin.is_(True)).first() is not None


def check_email(authenticate_email: str, to_update_email: str) -> bool:
    return authenticate_email == to_update_email


def can_user_update(db: Session, authenticate_email: str, to_update_email: str) -> bool:
    return any([is_user_admin(db, authenticate_email), check_email(authenticate_email, to_update_email)])


def check_password(password, hashed_password) -> bool:
    return verify_password(plain_password=password, hashed_password=hashed_password)


def check_authentication(db: Session, email: str, password: str) -> bool:
    model = User
    task = db.query(model).filter(model.email == email, model.deleted_at.is_(None)).first()
    if not task:
        raise HTTPException(400, "Email ou senha incorretos.")
    return check_password(password, task.hashed_password)


def validate_username_availability(username: str):
    model = User
    db: Session = SessionLocal()
    try:
        if db.query(model).filter(model.username == username, model.deleted_at.is_(None)).first():
            raise HTTPException(status_code=400, detail="Nome de usuário já está em uso.")
    finally:
        db.close()


def validate_email_availability(email: str):
    model = User
    db: Session = SessionLocal()
    try:
        if db.query(model).filter(model.email == email, model.deleted_at.is_(None)).first():
            raise HTTPException(status_code=400, detail="Email já está em uso.")
    finally:
        db.close()


def authenticate_user(db: Session, authentication_email: str, password: str):
    if not check_authentication(db, email=authentication_email, password=password):
        raise HTTPException(status_code=400, detail="Email ou senha incorretos.")


def check_user_privileges(db: Session, authentication_email: str, to_update_email: str):
    if not (is_user_admin(db, authentication_email) or check_email(authentication_email, to_update_email)):
        raise HTTPException(status_code=400, detail="Usuário sem privilégios para executar essa ação.")
