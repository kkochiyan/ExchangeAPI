import aiohttp

from app.core.config import settings
from app.exceptions.custom_exceptions import CustomHTTPException


class CurrencyApiClient:
    def __init__(self):
        self.base_url = settings.API_URL
        self.headers = {"apikey": settings.API_KEY}

    @staticmethod
    def delete_spases(currencies: str) -> str:
        while currencies.count(' '):
            currencies = currencies.replace(' ', '')
        return currencies

    async def _make_request(self, endpoint: str, params: dict = None) -> dict:
        url = f"{self.base_url}/{endpoint}"

        async with (aiohttp.ClientSession() as session):
            async with session.request(
                    "GET",
                    url,
                    headers=self.headers,
                    params=params,
                    ssl=False
            ) as response:

                if response.status != 200:
                    raise CustomHTTPException(status_code=response.status, detail=f"Статус ответа от API {response.status}")

                data = await response.json()

                if not data.get("success", True):
                    raise CustomHTTPException(status_code=400, detail='Запрос к API не удался')

                return data

    async def get_courses(self, source: str, currencies: str) -> dict:
        currencies_without_spases = self.delete_spases(currencies)
        data = await self._make_request("live", {"source": source, "currencies": currencies_without_spases})
        return data['quotes']

    async def get_names(self) -> dict:
        data = await self._make_request("list")
        return data['currencies']

    async def convert(self, to_currency: str, from_currency: str, amount: int) -> dict:
        data = await self._make_request(
            "convert",
            {"to": to_currency, "from": from_currency, "amount": amount}
        )
        return data


currency_client = CurrencyApiClient()
