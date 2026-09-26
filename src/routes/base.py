from fastapi import FastAPI , APIRouter , Depends
from dotenv import load_dotenv
from helpers.config import Settings ,  get_settings


base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get('/')
async def health_check(app_settings : Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "app_name": app_name,
        "Version": app_version
    }