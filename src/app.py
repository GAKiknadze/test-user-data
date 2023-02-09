from fastapi import FastAPI
from playhouse.db_url import connect

from .config import DB_URL
from .models import Country, User, UserContact, users_db
from .routes import router

app = FastAPI()

# Добавляемсозданный роутер
app.include_router(router)


@app.on_event("startup")
async def on_startup() -> None:
    """Инициализация подключения к базе данных
    и создание необходимых таблиц.
    """
    db = connect(DB_URL)
    users_db.initialize(db)
    db.create_tables([Country, User, UserContact])
