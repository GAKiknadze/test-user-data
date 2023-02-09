import os

# Настройки запуска сервера
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# Настройка подключения к базе данных
DB_URL = os.getenv("DB_URL")

# Настройки подлючения к API dadata.ru
# для работы сервиса (необходимо получить свой токен доступа на сайте)
DADATA_TOKEN = os.getenv("DADATA_TOKEN")
