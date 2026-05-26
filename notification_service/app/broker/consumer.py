import asyncio
import json
import logging
import os

import aio_pika

from app.db.database import AsyncSessionLocal
from app.models.notification import Notification
from app.websocket.manager import manager


logger = logging.getLogger(__name__)

RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://guest:guest@rabbitmq:5672/",
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


async def save_and_push_notification(
    user_id: int,
    title: str,
    message: str,
    event_type: str,
):
    async with AsyncSessionLocal() as db:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            event_type=event_type,
        )

        db.add(notification)
        await db.commit()
        await db.refresh(notification)

        await manager.send_to_user(
            user_id=notification.user_id,
            message=notification_to_message(notification),
        )


async def process_request_created(
    message: aio_pika.IncomingMessage,
):
    async with message.process():
        payload = json.loads(message.body.decode())

        await save_and_push_notification(
            user_id=payload["user_id"],
            title="Новая заявка",
            message=f"Создана новая заявка: {payload['title']}",
            event_type=payload["event_type"],
        )


async def process_request_status_changed(
    message: aio_pika.IncomingMessage,
):
    async with message.process():
        payload = json.loads(message.body.decode())

        await save_and_push_notification(
            user_id=payload["user_id"],
            title="Статус заявки изменён",
            message=(
                f"Ваша заявка теперь имеет статус: "
                f"{payload['status']}"
            ),
            event_type=payload["event_type"],
        )


async def process_news_created(
    message: aio_pika.IncomingMessage,
):
    async with message.process():
        payload = json.loads(message.body.decode())

        async with AsyncSessionLocal() as db:
            notifications = [
                Notification(
                    user_id=user_id,
                    title="Новая новость",
                    message=(
                        f"Опубликована новость: "
                        f"{payload['title']}"
                    ),
                    event_type=payload["event_type"],
                )
                for user_id in payload["user_ids"]
            ]

            db.add_all(notifications)
            await db.commit()

            for notification in notifications:
                await db.refresh(notification)

                await manager.send_to_user(
                    user_id=notification.user_id,
                    message=notification_to_message(notification),
                )


async def start_consumer():
    while True:
        try:
            connection = await aio_pika.connect_robust(
                RABBITMQ_URL
            )

            channel = await connection.channel()

            request_created_queue = await channel.declare_queue(
                "notifications.request_created",
                durable=True,
            )

            request_status_queue = await channel.declare_queue(
                "notifications.request_status_changed",
                durable=True,
            )

            news_queue = await channel.declare_queue(
                "notifications.news_created",
                durable=True,
            )

            await request_created_queue.consume(
                process_request_created
            )

            await request_status_queue.consume(
                process_request_status_changed
            )

            await news_queue.consume(
                process_news_created
            )

            logger.info("RabbitMQ consumers started")

            return

        except Exception as exc:
            logger.warning(
                "RabbitMQ is not ready, retrying in 5 seconds: %s",
                exc,
            )
            await asyncio.sleep(5)
