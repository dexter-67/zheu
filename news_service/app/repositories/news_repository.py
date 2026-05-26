from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.news import News
from app.schemas.news import NewsCreate, NewsUpdate


async def create_news(
    db: AsyncSession,
    news_data: NewsCreate,
    author_id: int,
) -> News:
    news = News(
        title=news_data.title,
        content=news_data.content,
        is_published=news_data.is_published,
        author_id=author_id,
    )

    db.add(news)
    await db.commit()
    await db.refresh(news)

    return news


async def get_news_list(db: AsyncSession) -> list[News]:
    result = await db.execute(
        select(News)
        .order_by(News.created_at.desc())
    )

    return list(result.scalars().all())


async def get_published_news_list(db: AsyncSession) -> list[News]:
    result = await db.execute(
        select(News)
        .where(News.is_published == True)
        .order_by(News.created_at.desc())
    )

    return list(result.scalars().all())


async def get_news_by_id(db: AsyncSession, news_id: int) -> News | None:
    result = await db.execute(
        select(News).where(News.id == news_id)
    )

    return result.scalar_one_or_none()


async def update_news(
    db: AsyncSession,
    news: News,
    news_data: NewsUpdate,
) -> News:
    update_data = news_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(news, field, value)

    await db.commit()
    await db.refresh(news)

    return news


async def delete_news(db: AsyncSession, news: News) -> None:
    await db.delete(news)
    await db.commit()
