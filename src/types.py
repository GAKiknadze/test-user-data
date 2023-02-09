import re


class RussianPhoneNumber(str):
    """Тип данных для российского номера телефона.
    Валидным является только тот номер, который:
    - начинается с 7
    - может содержать разделительные символы
    - должен содержать 11 цифр (включая 7 на первой позиции)
    """
    phone_pattern = "^7[\d\-\(\)\ ]{10,}$"
    phone_regexp = re.compile(phone_pattern)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=cls.phone_pattern,
            examples=[
                "79001112233",
                "7 9001112233",
                "7 900 000-00-00",
                "7(900) 111-2233",
                "7 (900) 000 00-00",
            ],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")

        m = cls.phone_regexp.fullmatch(v)
        if not m:
            raise ValueError("invalid phone number format")

        # Поиск цифр в строке
        phone_obj = re.sub("\D", "", m.group())

        phone = str(phone_obj)

        if len(phone) > 11:
            raise ValueError("invalid phone number format")

        return cls(phone)

    def __repr__(self):
        return f"RussianPhoneNumber({super().__repr__()})"


class CyrillicStr(str):
    """Тип данных, содержащий только символы кириллицы,
    тире, пробелы и точки.
    """
    cyrillic_pattern = "^([а-яА-Я\-\ \.]*)$"
    cyrillic_regexp = re.compile(cyrillic_pattern)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=cls.cyrillic_pattern,
            examples=[
                "Йоган",
                "автомобиль",
                "Йошкар-Ола",
                "Швейцарская Конфедерация"],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError("string required")

        m = cls.cyrillic_regexp.fullmatch(v)
        if not m:
            raise ValueError("invalid format")

        return cls(str(m.group()))

    def __repr__(self):
        return f"CyrillicStr({super().__repr__()})"
