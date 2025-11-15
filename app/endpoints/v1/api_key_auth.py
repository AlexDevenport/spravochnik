from fastapi import APIRouter, Header
from app.config import settings
from app.endpoints.v1.exceptions import InvalidApiKeyException


router = APIRouter(prefix="/v1", tags=["API-ключ"])

async def api_key_header(x_api_key: str = Header(...)) -> None:
    """Проверка API-ключа для всех защищённых эндпоинтов."""
    if x_api_key != settings.API_KEY:
        InvalidApiKeyException