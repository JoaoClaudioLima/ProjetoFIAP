from typing import Optional

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from src.model.schemas import UserInput, UserUpdateInput
from src.utils.database import get_db, authenticate_user, check_email_exists
from src.utils.user import create_new_db_user, get_db_user, delete_db_user, update_db_user

user_router = APIRouter()


@user_router.post("/user/", response_model=None, status_code=201)
def create_user(user: UserInput, db: Session = Depends(get_db)):
    # if check_email_exists(db, user.email):
    #     raise HTTPException(status_code=400, detail="Email already registered")
    create_new_db_user(user, db)
    return "Created"


@user_router.get("/user/", response_model=None)
def read_user(user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"), db: Session = Depends(get_db)):
    task = get_db_user(db, user_id=user_id)
    if not task:
        raise HTTPException(status_code=400, detail="User not found")
    return task


@user_router.delete("/user/", response_model=None, status_code=200)
def delete_user(user: UserUpdateInput, db: Session = Depends(get_db)):
    authenticate_user(db, user.authentication.email, user.to_update.email, user.authentication.password)
    task = delete_db_user(db, user=user)

    #  TODO update tarefas que este usuário tinha para sem usuário

    if not task:
        raise HTTPException(status_code=404, detail="User not found or already deleted")
    return "User deleted successfully"


@user_router.put("/user/", response_model=None)
def update_user(user: UserUpdateInput, db: Session = Depends(get_db)):


    authenticate_user(db, user.authentication.email, user.to_update.email, user.authentication.password)
    task = update_db_user(db=db, user=user)

    if not task:
        raise HTTPException(status_code=400, detail="User could not be updated")
    return "User updated successfully"
