from fastapi import FastAPI
import httpx
from sqlalchemy import text
from app.db.database import AsyncSessionLocal, engine
from contextlib import asynccontextmanager
from app.db.base import Base
from app.models.user import User
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.internal_users import router as internal_users_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(internal_users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


SERVICES = {
    "news-service": "http://news-service:8000",
    "notification-service": "http://notification-service:8000",
    "requests-service": "http://requests-service:8000"
}


@app.get('/')
async def health():
    return {
        'message': 'главный сервис работает'
    }


@app.get("/health/services")
async def check_services():
    results = {}

    async with httpx.AsyncClient(timeout=3.0) as client:
        for service_name, service_url in SERVICES.items():
            try:
                response = await client.get(service_url)
                results[service_name] = {
                    "status": "alive",
                    "code": response.status_code,
                    "response": response.json()
                }
            except Exception as error:
                results[service_name] = {
                    "status": "dead",
                    "error": str(error)
                }

    return {
        "core-service": "alive",
        "services": results
    }


@app.get('/health/db')
async def check_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT 1"))
        return {"database": "alive", "result": result.scalar()}
