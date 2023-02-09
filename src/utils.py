import random
import string

import aiohttp
import ujson

from .config import DADATA_TOKEN
from .schemas import Country

__POST_COUNTRY = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/country"


def random_string(length: int) -> str:
    """Функция создающая рандомные строчные значения длины-length.
    По техническому заданию определен только тип строковый тип идентификатора.
    
    Атрибут:
        length (int): длина рандомной строки
        
    Возвращает:
        (str): сгенерированную строку
    """
    letters = string.printable
    return "".join(random.choice(letters) for i in range(length))


async def search_country(value: str) -> Country | None:
    """Функция для поиска кода страны по подстроке на стороннем сервиса DADATA.ru

    Атрибут:
        value (str): название страны

    Возвращает:
        Country | None: необходимая инормация о стране
    """
    async with aiohttp.ClientSession(
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": "Token " + DADATA_TOKEN,
        }
    ) as session:        
        payload = ujson.dumps({"query": str(value), "count": 10})
        try:
            async with session.post(url=__POST_COUNTRY, data=payload) as response:
                status = response.status
                if status != 200:
                    return
                body = await response.json()
                suggestions = body.get("suggestions")
                if len(suggestions) != 1 or suggestions[0]["value"] != value:
                    return
                if suggestions[0]['unrestricted_value'] == value or suggestions[0]["value"] == value:
                    country = Country(
                        title=suggestions[0]["unrestricted_value"], code=suggestions[0]["data"]["code"]
                    )
                    return country
        except Exception:
            pass
