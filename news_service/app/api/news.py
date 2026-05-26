from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_payload, require_admin
from app.db.database import get_db
from app.schemas.news import NewsCreate, NewsRead, NewsUpdate
from app.services.news_service import (
    create_news_service,
    get_news_list_service,
    get_news_by_id_service,
    update_news_service,
    delete_news_service,
)


router = APIRouter(prefix="/news", tags=["news"])


@router.post("/", response_model=NewsRead)
async def create_news(
    news_data: NewsCreate,
    db: AsyncSession = Depends(get_db),
    admin_payload: dict = Depends(require_admin),
):
    return await create_news_service(
        db=db,
        news_data=news_data,
        author_id=int(admin_payload["sub"]),
    )


@router.get("/", response_model=list[NewsRead])
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await get_news_list_service(
        db=db,
        payload=payload,
    )


@router.get("/{news_id}", response_model=NewsRead)
async def get_news_by_id(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await get_news_by_id_service(
        db=db,
        news_id=news_id,
        payload=payload,
    )


@router.patch("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: int,
    news_data: NewsUpdate,
    db: AsyncSession = Depends(get_db),
    admin_payload: dict = Depends(require_admin),
):
    return await update_news_service(
        db=db,
        news_id=news_id,
        news_data=news_data,
    )


@router.delete("/{news_id}")
async def delete_news(
    news_id: int,
    db: AsyncSession = Depends(get_db),
    admin_payload: dict = Depends(require_admin),
):
    return await delete_news_service(
        db=db,
        news_id=news_id,
    )
