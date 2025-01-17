from fastapi import APIRouter

from src.controller.routes.task import tasks_router
from src.controller.routes.task_status import task_status_router
from src.controller.routes.user import users_router
from src.settings import Settings

router = APIRouter()

router.include_router(users_router, tags=["user"])
router.include_router(tasks_router, tags=["tasks"])
router.include_router(task_status_router, tags=["task_status"])


@router.get("/health-check",
            responses={
                200: {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "example": {
                                "version": "0.0.1",
                                "message": "Alive and kicking!"
                            }
                        }
                    }
                },
            },
            )
async def health_check():
    """
    Check de saúde do serviço.
    """
    data = {
        "version": Settings.VERSION,
        "message": "Alive and kicking!"
    }
    return data


@router.get("/")
async def home():
    """
    Landing page. Retorna uma string simples, sem funcionalidades.
    """
    data = {
        "message": "Hello World!"
    }
    return data
