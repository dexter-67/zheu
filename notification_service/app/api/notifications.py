from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user_payload
from app.db.database import get_db
from app.schemas.notification import NotificationCreate, NotificationRead
from app.services.notification_service import (
    create_notification_service,
    get_my_notifications_service,
    mark_notification_read_service,
)


router = APIRouter(
    prefix="/notifications",
    tags=["notifications"],
)


@router.post("/internal", response_model=NotificationRead)
async def create_notification_internal(
    notification_data: NotificationCreate,
    db: AsyncSession = Depends(get_db),
):
    return await create_notification_service(
        db=db,
        notification_data=notification_data,
    )


@router.get("/my", response_model=list[NotificationRead])
async def get_my_notifications(
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await get_my_notifications_service(
        db=db,
        user_id=int(payload["sub"]),
    )


@router.patch("/{notification_id}/read", response_model=NotificationRead)
async def mark_notification_read(
    notification_id: int,
    db: AsyncSession = Depends(get_db),
    payload: dict = Depends(get_current_user_payload),
):
    return await mark_notification_read_service(
        db=db,
        notification_id=notification_id,
        user_id=int(payload["sub"]),
    )
