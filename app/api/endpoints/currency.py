from fastapi import APIRouter, Depends, Request

from app.core.security import get_current_user
from app.utils.external_api import currency_client
from app.utils.response_formatter import format_response_courses, format_response_convert
from app.api.schemas.currency import SCoursesRes, SCurrencyNamesRes, SConvertRes, SCurrencyQuery, SConvertQuery
from app.limiter import limiter

router = APIRouter(
    prefix='/currency',
    tags=['Currency']
)

@router.get('/exchange')
@limiter.limit('10/minute')
async def get_current_courses(
        request: Request,
        query: SCurrencyQuery = Depends(),
        user: dict = Depends(get_current_user),
) -> list[SCoursesRes]:
    current_courses = await currency_client.get_courses(query.source, query.currencies)
    current_courses_response = format_response_courses(current_courses)
    return  current_courses_response


@router.get('/list')
@limiter.limit('5/minute')
async def get_currency_names(request: Request, user: dict = Depends(get_current_user)) -> SCurrencyNamesRes:
    currency_names = await currency_client.get_names()
    currency_names_response = SCurrencyNamesRes(all_names=currency_names)
    return currency_names_response


@router.get('/convert')
@limiter.limit('20/minute')
async def convert_currency(
        request: Request,
        query: SConvertQuery = Depends(),
        user: dict = Depends(get_current_user),
) -> SConvertRes:
    convert_result = await currency_client.convert(query.to_currency, query.from_currency, query.amount)
    convert_response = format_response_convert(convert_result)
    return convert_response
