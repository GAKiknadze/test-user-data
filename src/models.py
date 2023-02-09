import datetime

from peewee import CharField, DateField, ForeignKeyField, Model, Proxy

from .utils import random_string

users_db = Proxy()


class Country(Model):
    """Модель данных страны"""
    code = CharField(max_length=3, primary_key=True, unique=True)
    title = CharField(max_length=50, unique=True)

    class Meta:
        database = users_db


class User(Model):
    """Модель данных пользователя"""
    user_id = CharField(
        max_length=12, primary_key=True, unique=True, default=lambda: random_string(12)
    )
    name = CharField(max_length=50)
    surname = CharField(max_length=50)
    patronymic = CharField(max_length=50, null=True)

    country = ForeignKeyField(Country, backref="users")

    date_created = DateField(default=datetime.date.today())
    date_modified = DateField()

    def save(self, *args, **kwargs):
        self.date_modified = datetime.date.today()
        return super(User, self).save(*args, **kwargs)

    class Meta:
        database = users_db


class UserContact(Model):
    """Модель данных контактной информации о пользователе"""
    user = ForeignKeyField(
        User, primary_key=True, backref="contact", unique=True, on_delete="CASCADE"
    )
    phone_number = CharField(max_length=11, unique=True)
    email = CharField(max_length=255, null=True)

    class Meta:
        database = users_db
