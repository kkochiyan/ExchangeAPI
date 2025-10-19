from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError, ValidationException
from contextlib import asynccontextmanager
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.endpoints.currency import router as router_currency
from app.api.endpoints.users import router as router_users
from app.exceptions.exception_handling import (custom_http_exception_handler,
                                               custom_request_validation_exception_handler,
                                               custom_exception_handler)

from app.logger import my_logger
from app.limiter import init_limiter


@asynccontextmanager
async def lifespan(_: FastAPI):
    my_logger.info('Начало работы приложения')
    yield
    my_logger.info('Конец работы приложения')

app = FastAPI(lifespan=lifespan)

init_limiter(app)

app.include_router(router_users)
app.include_router(router_currency)

app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, custom_request_validation_exception_handler)
app.add_exception_handler(ValidationException, custom_request_validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(Exception, custom_exception_handler)


