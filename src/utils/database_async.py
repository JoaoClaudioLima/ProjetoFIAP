from typing import Union, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.future import select
from sqlalchemy import create_engine

from src.model.database import User

# Defina a constante DATABASE_URL diretamente aqui
DATABASE_URL = "postgresql+psycopg://user:password@postgres_db:5432/mydatabase"

# Engine assíncrona para FastAPI
async_engine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

# Engine síncrona para Celery e outras operações que não suportam async
sync_engine = create_engine(DATABASE_URL.replace("postgresql+psycopg", "postgresql"), future=True)
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

def get_async_db():
    """Gera uma sessão de banco de dados assíncrona para uso no FastAPI."""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()

async def db_read_user(
    db: AsyncSession, # Use `AsyncSession` para sessões assíncronas
    user_id: Union[int, None] = None,
    skip: int = 0,
    limit: int = 10
):
    """Lê usuários do banco de dados de forma assíncrona."""
    model = User

    if not user_id:
        result = await db.execute(
            select(model).filter(model.deleted_at.is_(None)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    result = await db.execute(select(model).filter(model.id == user_id))
    return result.scalars().all()


def db_read_user_sync(
    db: Session,  # Use `Session` para sessões síncronas
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
):
    """Lê usuários do banco de dados de forma síncrona."""
    model = User

    if not user_id:
        result = db.execute(
            select(model).filter(model.deleted_at.is_(None)).offset(skip).limit(limit)
        )
        return result.scalars().all()

    result = db.execute(select(model).filter(model.id == user_id))
    return result.scalars().all()