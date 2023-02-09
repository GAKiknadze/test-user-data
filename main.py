import uvicorn

from src.app import app
from src.config import HOST, PORT

if __name__ == "__main__":
    # Запускаем веб-приложение
    uvicorn.run(app, host=HOST, port=PORT)
