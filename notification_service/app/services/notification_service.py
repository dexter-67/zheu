from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.notification_repository import (
    create_notification,
    get_user_notifications,
    get_notification_by_id,
    update_notification,
)
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)
from app.websocket.manager import manager


async def create_notification_service(
    db: AsyncSession,
    notification_data: NotificationCreate,
):
    notification = await create_notification(
        db=db,
        notification_data=notification_data,
    )

    await manager.send_to_user(
        user_id=notification.user_id,
        message={
            "id": notification.id,
            "user_id": notification.user_id,
            "title": notification.title,
            "message": notification.message,
            "event_type": notification.event_type,
            "is_read": notification.is_read,
            "created_at": str(notification.created_at),
        },
    )

    return notification


async def get_my_notifications_service(
    db: AsyncSession,
    user_id: int,
):
    return await get_user_notifications(
        db=db,
        user_id=user_id,
    )


async def mark_notification_read_service(
    db: AsyncSession,
    notification_id: int,
    user_id: int,
):
    notification = await get_notification_by_id(
        db=db,
        notification_id=notification_id,
    )

    if notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Уведомление не найдено",
        )

    if notification.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к уведомлению",
        )

    notification_data = NotificationUpdate(
        is_read=True,
    )

    return await update_notification(
        db=db,
        notification=notification,
        notification_data=notification_data,
    )
