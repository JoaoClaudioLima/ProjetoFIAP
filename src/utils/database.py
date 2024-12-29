from sqlalchemy.orm import Session


def get_from_db(model, db: Session, skip: int = 0, limit: int = 10):
    return db.query(model).offset(skip).limit(limit).all()


def get_from_db_filter_id(model, db: Session, table_id: str = None):
    return db.query(model).filter(model.id == table_id).first()
