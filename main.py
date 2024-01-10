from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.bd_handlers import db_router
from api.local_handlers import local_router

# Развёртка API
app = FastAPI(title="Analysis API")

# Основной путь
main_api_router = APIRouter()


# Добавление побочных путей
# db - путь для работы с БД
# local - путь для получения статичных данных
main_api_router.include_router(db_router, prefix="/db", tags=["db"])
main_api_router.include_router(local_router, prefix="/local", tags=["local"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # Параметры запуска сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)