from typing import Optional

from fastapi import Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from src.model.models import UserInput
from src.utils.database import get_db
from src.utils.user import get_user_from_db, create_new_user, validate_user_input

user_router = APIRouter()


@user_router.post("/user/", response_model=None, status_code=201)
def create_task(user: UserInput, db: Session = Depends(get_db)):
    validate_user_input(user, db)
    create_new_user(user, db)
    return "OK"


@user_router.get("/user/", response_model=None)
def read_user(user_id: Optional[int] = Query(None, description="The ID of the user to retrieve"), db: Session = Depends(get_db)):

    task, message = get_user_from_db(db, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail=message)
    return task
