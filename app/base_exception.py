from dataclasses import dataclass
from fastapi import HTTPException


@dataclass(kw_only=True)
class BaseAppException(HTTPException):

    status_code: int
    detail: str

    def __post_init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)