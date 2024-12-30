from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from src.controller.database import Base


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status_id = Column(Integer, ForeignKey('task_status.id'))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    status = relationship("TaskStatus", back_populates="tasks")
    user = relationship("User", back_populates="tasks")


class TaskStatus(Base):
    __tablename__ = "task_status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="status")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    is_admin = Column(Boolean, index=True, default=False, nullable=False)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, server_default=None)

    tasks = relationship("Task", back_populates="user")


class UserInput(BaseModel):
    username: str
    email: str
    full_name: str
    password: str
    # TODO criar validação de email e password
