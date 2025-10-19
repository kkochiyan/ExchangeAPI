from fastapi import APIRouter, Response, Request

from app.api.schemas.user import SUserAuth, SAuthRes
from app.core.security import authenticate_user, create_jwt_token, get_hashed_password
from app.db.database import add, find_one_or_none
from app.exceptions.custom_exceptions import CustomHTTPException
from app.limiter import limiter


router = APIRouter(
    prefix="/users/auth",
    tags=['Auth']
)

@router.post("/register")
@limiter.limit('2/minute')
async def reg_user(request: Request, user_data: SUserAuth) -> SAuthRes:
    existing_user = find_one_or_none(user_data.username)
    if existing_user:
        raise CustomHTTPException(detail='Пользователь уже существует', status_code=409)
    hashed_password = get_hashed_password(user_data.password)
    add(user_data.username, hashed_password)
    register_response = SAuthRes(message="Вы успешно зарегестрированы")
    return register_response


@router.post("/login")
@limiter.limit('5/minute')
async def login(request: Request ,response: Response, user_data: SUserAuth) -> SAuthRes:
    user = authenticate_user(user_data)
    access_token = create_jwt_token({"sub": user['username']})
    response.set_cookie("access_token", access_token)
    login_response = SAuthRes(message="Вы успешно авторизированы")
    return login_response


@router.post("/logout")
async def logout(response: Response) -> SAuthRes:
    response.delete_cookie("access_token")
    logout_response = SAuthRes(message='Вы вышли из аккаунта')
    return logout_response
