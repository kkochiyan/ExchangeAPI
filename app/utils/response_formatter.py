from app.api.schemas.currency import SCoursesRes, SConvertRes

def format_response_courses(courses: dict) -> list[SCoursesRes]:
    BASE_CURRENCY_AMOUNT = 1

    response = []

    for currency_pair, amount in courses.items():
        base_currency = currency_pair[:3]
        currency = currency_pair[3:]

        courses_response = SCoursesRes(
            from_amount_currency=f'{BASE_CURRENCY_AMOUNT} {base_currency}',
            to_amount_currency=f'{amount} {currency}'
        )

        response.append(courses_response)

    return response


def format_response_convert(convert_data: dict) -> SConvertRes:
    from_amount = convert_data['query']['amount']
    from_currency = convert_data['query']['from']
    to_currency = convert_data['query']['to']
    to_amount = convert_data['result']

    convet_response = SConvertRes(
        from_amount_currency=f'{from_amount} {from_currency}',
        to_amount_currency=f'{to_amount} {to_currency}'
    )

    return convet_response