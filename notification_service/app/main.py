import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.notification import Notification
from app.db.base import Base
from app.db.database import engine
from app.api.notifications import router as notification_router
from app.api.websocket_notifications import router as websocket_router
from app.api.internal_notification import router as internal_notification_router
from app.broker.consumer import start_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(start_consumer())

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://192.168.0.111:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notification_router)
app.include_router(websocket_router)
app.include_router(internal_notification_router)


@app.get("/")
async def health():
    return {
        "status": "ok"
    }
