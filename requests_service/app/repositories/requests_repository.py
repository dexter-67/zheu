from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.request import Request
from app.schemas.request import RequestCreate, RequestUpdate


async def create_request(
    db: AsyncSession,
    request_data: RequestCreate,
    author_id: int,
) -> Request:
    request = Request(
        title=request_data.title,
        content=request_data.content,
        author_id=author_id,
    )

    db.add(request)
    await db.commit()
    await db.refresh(request)

    return request


async def get_all_requests(db: AsyncSession) -> list[Request]:
    result = await db.execute(
        select(Request).order_by(Request.created_at.desc())
    )
    return list(result.scalars().all())


async def get_requests_by_author(
    db: AsyncSession,
    author_id: int,
) -> list[Request]:
    result = await db.execute(
        select(Request)
        .where(Request.author_id == author_id)
        .order_by(Request.created_at.desc())
    )
    return list(result.scalars().all())


async def get_request_by_id(
    db: AsyncSession,
    request_id: int,
) -> Request | None:
    result = await db.execute(
        select(Request).where(Request.id == request_id)
    )
    return result.scalar_one_or_none()


async def update_request(
    db: AsyncSession,
    request: Request,
    request_data: RequestUpdate,
) -> Request:
    update_data = request_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(request, field, value)

    await db.commit()
    await db.refresh(request)

    return request


async def delete_request(
    db: AsyncSession,
    request: Request,
) -> None:
    await db.delete(request)
    await db.commit()
