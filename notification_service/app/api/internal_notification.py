from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.internal_security import verify_internal_token
from app.db.database import get_db
from app.models.notification import Notification
from app.schemas.notification import (
    InternalNotificationCreate,
    BulkNotificationCreate,
)
from app.websocket.manager import manager


router = APIRouter(
    prefix="/notifications/internal",
    tags=["internal-notifications"],
)


def notification_to_message(notification: Notification) -> dict:
    return {
        "id": notification.id,
        "user_id": notification.user_id,
        "title": notification.title,
        "message": notification.message,
        "event_type": notification.event_type,
        "is_read": notification.is_read,
        "created_at": str(notification.created_at),
    }


@router.post(
    "",
    dependencies=[Depends(verify_internal_token)],
)
async def create_internal_notification(
    notification_data: InternalNotificationCreate,
    db: AsyncSession = Depends(get_db),
):
    notification = Notification(
        user_id=notification_data.user_id,
        title=notification_data.title,
        message=notification_data.message,
        event_type=notification_data.event_type,
    )

    db.add(notification)

    await db.commit()
    await db.refresh(notification)

    await manager.send_to_user(
        user_id=notification.user_id,
        message=notification_to_message(notification),
    )

    return notification


@router.post(
    "/bulk",
    dependencies=[Depends(verify_internal_token)],
)
async def create_bulk_notifications(
    notification_data: BulkNotificationCreate,
    db: AsyncSession = Depends(get_db),
):
    notifications = [
        Notification(
            user_id=user_id,
            title=notification_data.title,
            message=notification_data.message,
            event_type=notification_data.event_type,
        )
        for user_id in notification_data.user_ids
    ]

    db.add_all(notifications)

    await db.commit()

    for notification in notifications:
        await db.refresh(notification)

        await manager.send_to_user(
            user_id=notification.user_id,
            message=notification_to_message(notification),
        )

    return {
        "message": "Bulk notifications created",
        "count": len(notifications),
    }
