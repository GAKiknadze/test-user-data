from fastapi import APIRouter, Body, HTTPException, status
from fastapi.responses import Response

from .logic import (
    create_country,
    create_or_update_user,
    delete_user_by_phone_number,
    get_country,
    get_user_info_by_phone_number,
)
from .schemas import PhoneNumber, UserIn, UserOut
from .utils import search_country

router = APIRouter()


@router.post(
    "/save_user_data",
    responses={404: {"description": "The country was not found"}},
    status_code=status.HTTP_201_CREATED,
)
async def save_user_data(user: UserIn = Body()):
    """Создать или обновить пользователя"""
    country_obj = get_country(user.country)
    if country_obj is None:
        country = await search_country(user.country)
        if country is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        country_obj = create_country(country.title, country.code)
    create_or_update_user(user, country_obj)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post(
    "/get_user_data",
    response_model=UserOut,
    responses={404: {"description": "The user was not found"}},
    status_code=status.HTTP_200_OK,
)
async def get_user_data(phone_number: PhoneNumber = Body()):
    """Получить информацию о пользователе по номеру телефона"""
    user = get_user_info_by_phone_number(phone_number.phone_number)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.post(
    "/delete_user_data",
    responses={404: {"description": "The user was not found"}},
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_data(phone_number: PhoneNumber = Body()):
    """Удалить пользователя по номеру телефона"""
    result = delete_user_by_phone_number(phone_number.phone_number)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
