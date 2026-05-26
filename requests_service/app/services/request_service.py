from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.broker.rabbitmq import publish_event
from app.repositories.requests_repository import (
    create_request,
    get_request_by_id,
    get_all_requests,
    get_requests_by_author,
    update_request,
    delete_request,
)

from app.schemas.request import (
    RequestCreate,
    RequestUpdate,
)


def is_admin(payload: dict) -> bool:
    return payload.get("role") == "admin"


async def create_request_service(
    db: AsyncSession,
    request_data: RequestCreate,
    author_id: int,
):
    request = await create_request(
        db=db,
        request_data=request_data,
        author_id=author_id,
    )

    await publish_event(
        queue_name="notifications.request_created",
        payload={
            "request_id": request.id,
            "user_id": 1,
            "title": request.title,
            "event_type": "request_created",
        },
    )

    return request


async def get_all_requests_service(
    db: AsyncSession,
):
    return await get_all_requests(db)


async def get_my_requests_service(
    db: AsyncSession,
    author_id: int,
):
    return await get_requests_by_author(
        db=db,
        author_id=author_id,
    )


async def get_request_by_id_service(
    db: AsyncSession,
    request_id: int,
    payload: dict,
):
    request = await get_request_by_id(
        db=db,
        request_id=request_id,
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    if (
        not is_admin(payload)
        and request.author_id != int(payload["sub"])
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заявке",
        )

    return request


async def update_request_service(
    db: AsyncSession,
    request_id: int,
    request_data: RequestUpdate,
):
    request = await get_request_by_id(
        db=db,
        request_id=request_id,
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    old_status = request.status

    updated_request = await update_request(
        db=db,
        request=request,
        request_data=request_data,
    )

    if (
        request_data.status is not None
        and updated_request.status != old_status
    ):
        await publish_event(
            queue_name="notifications.request_status_changed",
            payload={
                "request_id": updated_request.id,
                "user_id": updated_request.author_id,
                "status": updated_request.status,
                "event_type": "request_status_changed",
            },
        )

    return updated_request


async def delete_request_service(
    db: AsyncSession,
    request_id: int,
):
    request = await get_request_by_id(
        db=db,
        request_id=request_id,
    )

    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заявка не найдена",
        )

    await delete_request(
        db=db,
        request=request,
    )

    return {"message": "Заявка удалена"}
