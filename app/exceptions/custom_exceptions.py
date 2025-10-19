from fastapi.exceptions import HTTPException, ValidationException
from typing import Optional

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)

class CustomValidationException(ValidationException):
    def __init__(self, message: str, field: str = None, code: str = "value_error"):
        errors = [{
            'loc': (field,) if field else ('body',),
            'msg': message,
            'type': code
        }]
        super().__init__(errors)