from pydantic import BaseModel, constr


class SUserAuth(BaseModel):
    username: str
    password: str

class SAuthRes(BaseModel):
    message: str
