from fastapi import APIRouter

from src.controller.routes.task import task_router
from src.controller.routes.task_status import task_status_router
from src.controller.routes.user import user_router
from src.settings import Settings

router = APIRouter()

router.include_router(user_router, tags=["user"])
# router.include_router(task_router, tags=["task"])
# router.include_router(task_status_router, tags=["task_status"])


@router.get("/health-check")
async def health_check():
    '''
    Check de saúde do serviço.
    '''
    data = {
        "version": Settings.VERSION,
        "message": "Alive and kicking!"
    }
    return data


@router.get("/")
async def home():
    data = {
        "message": "Hello World!"
    }
    return data
