from pydantic import BaseModel, field_validator, Field
from app.exceptions.custom_exceptions import CustomValidationException

class SCoursesRes(BaseModel):
    from_amount_currency: str
    to_amount_currency: str

class SCurrencyNamesRes(BaseModel):
    all_names: dict

class SConvertRes(SCoursesRes):
    pass


class SCurrencyQuery(BaseModel):
    source: str = Field(..., description='Введите валюту, для которых хотите получить курс')
    currencies: str = Field(...,description='Введите через запятую валюты, по отнешению к которым будет вычисляться курс')

    @field_validator('source')
    @classmethod
    def validate_source(cls, v: str) -> str:
        if not v.isalpha() or len(v) != 3:
            raise CustomValidationException(
                message='Базовая валюта должна состоять из 3-х букв',
                field='source',
                code='value_error.currency_format'
            )
        return v.upper()

    @field_validator('currencies')
    @classmethod
    def validate_currencies(cls, v: str) -> str:
        codes = v.split(',')
        for code in codes:
            if not code.strip().isalpha() or len(code.strip()) != 3:
                raise CustomValidationException(
                    message='Все валюты должны состоять из 3-х букв',
                    field='currencies',
                    code='value_error.currency_format'
                )
        return v.upper()


class SConvertQuery(BaseModel):
    to_currency: str = Field(..., description='Введите валюту в которую хотите конвертировать')
    from_currency: str = Field(..., description='Введите валюту которую хотите конвертировать')
    amount: int = Field(1, ge=1, description='Введите количество конвертируемой валюты (по умолчанию 1)')

    @field_validator('to_currency', 'from_currency')
    @classmethod
    def validate_currency_codes(cls, v: str) -> str:
        v = v.strip().upper()
        if not v.isalpha() or len(v) != 3:
            raise CustomValidationException(
                message='Базовая валюта должна состоять из 3-х букв',
                field='source',
                code='value_error.currency_format'
            )
        return v