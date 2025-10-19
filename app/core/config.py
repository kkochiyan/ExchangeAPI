from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    MODE: Literal['TEST', 'DEV', 'PROD']

    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    API_KEY: str
    API_URL: str


settings = Settings()
