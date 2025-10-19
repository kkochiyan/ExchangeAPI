from pydantic import BaseModel
from typing import Optional, List

class SCustomHTTPException(BaseModel):
    status_code: int
    er_details: Optional[str] = None

class SValidationErrorItem(BaseModel):
    field: str
    message: str
    code: str

class SValidationErrorResponse(BaseModel):
    url: str
    title: str = "Validation Error"
    status: int = 422
    detail: Optional[str] = "The request body failed validation."
    instance: str
    errors: Optional[List[SValidationErrorItem]] = None



