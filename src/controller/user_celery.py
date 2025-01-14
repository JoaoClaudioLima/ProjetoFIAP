from celery import Celery
from src.utils.database import get_db  # Método que retorna uma sessão do banco
from src.utils.user import db_read_user  # Função que faz a lógica de leitura do usuário no banco

# Importa a instância do Celery
from src.controller.celery_app import celery_app

@celery_app.task(name="get_user_task")
def get_user_task(user_id: int):
    # Create a manual database session
    db = get_db()
    try:
        # Fetch user data
        users = db_read_user(db, user_id=user_id)
        return users
    finally:
        db.close()