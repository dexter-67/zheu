from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.core_client import get_resident_users
from app.broker.rabbitmq import publish_event
from app.repositories.news_repository import (
    create_news,
    get_news_by_id,
    get_news_list,
    get_published_news_list,
    update_news,
    delete_news,
)
from app.schemas.news import NewsCreate, NewsUpdate


async def create_news_service(
    db: AsyncSession,
    news_data: NewsCreate,
    author_id: int,
):
    created_news = await create_news(
        db=db,
        news_data=news_data,
        author_id=author_id,
    )

    if created_news.is_published:
        users = await get_resident_users()

        user_ids = [
            user["id"]
            for user in users
        ]

        await publish_event(
            queue_name="notifications.news_created",
            payload={
                "news_id": created_news.id,
                "title": created_news.title,
                "user_ids": user_ids,
                "event_type": "news_created",
            },
        )

    return created_news


async def get_news_list_service(
    db: AsyncSession,
    payload: dict,
):
    role = payload.get("role")

    if role == "admin":
        return await get_news_list(db)

    return await get_published_news_list(db)


async def get_news_by_id_service(
    db: AsyncSession,
    news_id: int,
    payload: dict | None = None,
):
    news = await get_news_by_id(db=db, news_id=news_id)

    if news is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Новость не найдена",
        )

    if payload is not None:
        role = payload.get("role")

        if role != "admin" and not news.is_published:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Новость не найдена",
            )

    return news


async def update_news_service(
    db: AsyncSession,
    news_id: int,
    news_data: NewsUpdate,
):
    news = await get_news_by_id_service(
        db=db,
        news_id=news_id,
    )

    return await update_news(
        db=db,
        news=news,
        news_data=news_data,
    )


async def delete_news_service(db: AsyncSession, news_id: int):
    news = await get_news_by_id_service(
        db=db,
        news_id=news_id,
    )

    await delete_news(db=db, news=news)

    return {"message": "Новость удалена"}
