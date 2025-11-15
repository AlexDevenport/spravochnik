from dataclasses import dataclass
from fastapi import status
from app.base_exception import BaseAppException


@dataclass(kw_only=True)
class InvalidApiKeyException(BaseAppException):

    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Неправильный API-ключ"


@dataclass(kw_only=True)
class OrganizationNotFoundException(BaseAppException):

    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = "Организация не найдена"