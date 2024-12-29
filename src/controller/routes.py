from fastapi import APIRouter

from src.settings import Settings

router = APIRouter()


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


@router.post("/create-object")
async def create_object():
    data = {
        "message": "Hello World!"
    }
    return data