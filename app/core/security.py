import bcrypt
import jwt
from fastapi import Depends, Request
from datetime import datetime, timedelta, timezone

from app.api.schemas.user import SUserAuth
from app.core.config import settings
from app.db.database import find_one_or_none
from app.exceptions.custom_exceptions import CustomHTTPException


def veify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_hashed_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


def authenticate_user(user_data: SUserAuth) -> dict | None:
    user = find_one_or_none(user_data.username)
    if not (user and veify_password(user_data.password, user['hashed_password'])):
        raise CustomHTTPException(detail='Неверный логин или пароль', status_code=401)
    return user


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise CustomHTTPException(detail='Токен отсутствует', status_code=401)
    return token


def get_current_user(token: str = Depends(get_token)) -> dict:
    try:
        decode_jwt = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except jwt.DecodeError:
        raise CustomHTTPException(detail='Неверный формат токена', status_code=401)
    except jwt.ExpiredSignatureError:
        raise CustomHTTPException(detail='Токен истек', status_code=401)
    username = decode_jwt.get("sub")
    if not username:
        raise CustomHTTPException(status_code=401)
    user = find_one_or_none(username)
    if not user:
        raise CustomHTTPException(status_code=401)

    return user
