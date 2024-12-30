from sqlalchemy.orm import Session

from src.controller.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_from_db(model, db: Session, skip: int = 0, limit: int = 10):
    return db.query(model).offset(skip).limit(limit).all()
