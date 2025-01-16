import json
from typing import Optional

from celery import Celery
from src.utils.database_async import SyncSessionLocal, db_read_user_sync
from src.controller.celery_app import celery_app
from sqlalchemy.orm import class_mapper

def serialize_sqlalchemy_object(obj):
    """
    Serializa um objeto SQLAlchemy em um formato JSON serializável.
    """
    columns = [column.key for column in class_mapper(obj.__class__).columns]
    return {key: getattr(obj, key) for key in columns}

@celery_app.task(name="get_user_task")
def get_user_task(user_id: Optional[int] = None):
    try:
        with SyncSessionLocal() as db:  # Sessão síncrona
            users = db_read_user_sync(db, user_id=user_id)  # Use a versão síncrona
            serialized_users = [serialize_sqlalchemy_object(user) for user in users]
            return serialized_users
    except Exception as e:
        return {"error": str(e)}