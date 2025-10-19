import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.exceptions.exception_schemas import SCustomHTTPException, SValidationErrorItem, SValidationErrorResponse
from app.logger import my_logger


def custom_http_exception_handler(request, exc):
    my_logger.warning(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else None
    )
    error = jsonable_encoder(SCustomHTTPException(status_code=exc.status_code, er_details=exc.detail))
    return JSONResponse(status_code=exc.status_code, content=error)


def custom_request_validation_exception_handler(request: Request, exc):
    my_logger.info(
        "Request validation failed",
        method=request.method,
        path=request.url.path,
        errors_count=len(exc.errors()),
        errors=[{"field": ".".join(str(loc) for loc in error["loc"] if loc != "body"), "type": error["type"]}
                for error in exc.errors()]
    )

    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        if not field:
            field = "body"

        errors.append(SValidationErrorItem(
            field=field,
            message=error["msg"],
            code=error["type"]
        ))

    error_response = jsonable_encoder(SValidationErrorResponse(
        url=str(request.url),
        instance=str(request.url.path),
        errors=errors if errors else None
    ))

    return JSONResponse(
        status_code=422,
        content=error_response,
        headers={"Content-Type": "application/problem+json"}
    )

def custom_exception_handler(request, exc):
    my_logger.error(
        "Unhandled exception occurred",
        exception_type=type(exc).__name__,
        exception_message=str(exc),
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host if request.client else None,
        traceback=traceback.format_exc()
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "type": type(exc).__name__,
            "traceback": traceback.format_exc(),  # Только для development!
            "endpoint": str(request.url),
            "method": request.method
        }
    )

