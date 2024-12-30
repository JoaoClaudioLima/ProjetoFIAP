# from typing import Optional
#
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
#
# from src.controller.database import SessionLocal
# from src.model import models
# from src.model.models import UserInput
# from src.settings import Settings
#
# from src.utils.database import get_from_db
# from src.utils.task import get_task_from_db
# from src.utils.user import create_user, get_user_from_db
#
# router = APIRouter()
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# @router.get("/health-check")
# async def health_check():
#     '''
#     Check de saúde do serviço.
#     '''
#     data = {
#         "version": Settings.VERSION,
#         "message": "Alive and kicking!"
#     }
#     return data
#
#
# @router.get("/")
# async def home():
#     data = {
#         "message": "Hello World!"
#     }
#     return data
#
#
# # CRUD for task_status table
#
# @router.get("/task-status/", response_model=None)
# def read_task_status(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     task_status = get_from_db(models.TaskStatus, db, skip=skip, limit=limit)
#     return task_status
#
#
# # CRUD for user table
#
# @router.post("/user/", response_model=None, status_code=201)
# def create_task(user: UserInput, db: Session = Depends(get_db)):
#     create_user(user, db)
#     return "OK"
#
#
# @router.get("/user/", response_model=None)
# def read_user(user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"), db: Session = Depends(get_db)):
#
#     task = get_user_from_db(db, user_id=user_id)
#     if not task:
#         raise HTTPException(status_code=404, detail="User not found")
#     return task
#
#
# # CRUD for task table
# @router.get("/tasks/", response_model=None)
# def read_tasks(
#         user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"),
#         status_id: Optional[int] = Query(None, description="The ID of the status to retrieve"),
#         task_id: Optional[int] = Query(None, description="The ID of the task to retrieve"),
#         skip: int = 0,
#         db: Session = Depends(get_db)
#     ):
#     query_params = [user_id, status_id, task_id]
#
#     if any([user_id, status_id, task_id]):
#         task = get_task_from_db(db=db, user_id=user_id, status_id=status_id, task_id=task_id)
#         return task
#
#     tasks = get_from_db(models.Task, db, skip=skip)
#     return tasks
