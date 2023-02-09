from pydantic import BaseModel, EmailStr, Field, validator

from .types import CyrillicStr, RussianPhoneNumber


class UserIn(BaseModel):
    """Схема данных о пользователе для проверки тела запроса

    Атрибуты:
        name (CyrillicStr): Имя
        surname (CyrillicStr): Фамилия
        patronyc (CyrillicStr | None) = None: Отчество (опционально)
        phone_number (RussianPhoneNumber): Номер телефона начинающийся с 7
        email (EmailStr | None) = None: Адрес электронной почты (опционально)
        country (CyrillicStr): Страна
    """
    name: CyrillicStr
    surname: CyrillicStr
    patronymic: CyrillicStr | None = Field(default=None)
    phone_number: RussianPhoneNumber
    email: EmailStr | None = Field(default=None)
    country: CyrillicStr

    @validator("name", "surname", "patronymic", "country")
    def validate_(cls, v) -> str:
        """Проверяем, что длина строк не более 50-ти символов"""
        if len(v) > 50:
            raise ValueError(
                'the maximum length of the string should be 50 characters')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Имя",
                "surname": "Фамилия",
                "patronymic": "Отчество",
                "phone_number": "71234567890",
                "email": "some@email.address",
                "country": "Страна",
            }
        }


class UserOut(BaseModel):
    """Схема данных о пользователе для отправки в теле ответа от сервера.
    Т.к. передаваемые клиенту данные жестко прописаны, не целесообразно
    применять более жесткую проверку типов данных.

    Атрибуты:
        name (str): Имя
        surname (str): Фамилия
        patronyc (str) = "": Отчество (опционально)
        phone_number (str): Номер телефона начинающийся с 7
        email (str | None) = None: Адрес электронной почты (опционально)
        country (str): Страна
    """
    name: str
    surname: str
    patronymic: str | None = Field(default="")
    phone_number: str
    email: str | None = Field(default=None)
    country: str
    country_code: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Имя",
                "surname": "Фамилия",
                "patronymic": "Отчество",
                "phone_number": "71234567890",
                "email": "some@email.address",
                "country": "Страна",
                "country_code": "123",
            }
        }


class PhoneNumber(BaseModel):
    """Схема данных тела запроса для номера телефона

    Атрибуты:
        phone_number (RussianPhoneNumber): Номер телефона начинающийся с 7
    """
    phone_number: RussianPhoneNumber

    class Config:
        schema_extra = {"example": {"phone_number": "71234567890"}}


class Country(BaseModel):
    """Схема для удобной работы с функциями

    Атрибуты:
        title (str): Название страны
        code (str): Код страны
    """
    title: str
    code: str
