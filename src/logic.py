from .models import Country, User, UserContact
from .schemas import RussianPhoneNumber, UserIn, UserOut


def get_country(title: str) -> Country | None:
    """Получить информацию о стране по ее названию

    Атрибуты:
        title (str): название страны

    Возвращает:
        Country | None: информация о стране
    """
    return Country.get_or_none(Country.title == title)


def create_country(title: str, code: str) -> Country:
    """Добавить и получить информацию о стране

    Атрибуты:
        title (str): название страны
        code (str): код страны

    Возвращает:
        Country: информация о стране
    """
    country = Country.create(title=title, code=code)
    country.save()
    return country


def get_user_info_by_phone_number(
    phone_number: RussianPhoneNumber
) -> UserOut | None:
    """Получить информацию о пользователе по номеру телефона

    Атрибут:
        phone_number (RussianPhoneNumber): российский номер телефона

    Возвращает:
        UserOut | None: информация о пользователе
        преобразованная для отправки клиентам сервиса. В случае, когда
        пользователь не найден возвращается None.
    """
    user = None
    contact_obj = UserContact.get_or_none(UserContact.phone_number == phone_number)
    if contact_obj is not None:
        user = UserOut(
            name=contact_obj.user.name,
            surname=contact_obj.user.surname,
            patronymic=contact_obj.user.patronymic,
            phone_number=contact_obj.phone_number,
            email=contact_obj.email,
            country=contact_obj.user.country.title,
            country_code=contact_obj.user.country.code,
        )
    return user


def create_or_update_user(user: UserIn, country_obj: Country) -> None:
    """Создает или обновляет информацию о пользователе

    Атрибуты:
        user (UserIn): данные о пользователе
        country_obj (Country): данные о стране
    """
    contact_obj = UserContact.get_or_none(UserContact.phone_number == user.phone_number)

    if contact_obj is not None:
        # Если пользователь был найден по номеру телефона
        # Обновляем контактную информацию
        contact_obj.email = user.email
        contact_obj.save()
        # Обновляем основную информацию
        contact_obj.user.update(
            {
                User.name: user.name,
                User.surname: user.surname,
                User.patronymic: user.patronymic,
                User.country: country_obj,
            }
        ).where(User.user_id == contact_obj.user_id).execute()
    else:
        # Создаем нового пользователя
        user_obj = User.create(
            name=user.name,
            surname=user.surname,
            patronymic=user.patronymic,
            country=country_obj,
        )
        # Создаем контактную информацию о пользователе
        contact_obj = UserContact.create(
            user=user_obj, phone_number=user.phone_number, email=user.email
        )
    contact_obj.save()


def delete_user_by_phone_number(phone_number: RussianPhoneNumber) -> bool:
    """Удаляет информацию о пользователе по номеру телефона

    Атрибут:
        phone_number (RussianPhoneNumber): российский номер телефона

    Возвращает:
        bool: Если пользователь был удален возращает True, иначе False
    """
    result = False
    contact_obj = UserContact.get_or_none(UserContact.phone_number == phone_number)
    if contact_obj is not None:
        User.delete().where(User.user_id == contact_obj.user_id).execute()
        result = True
    return result
