import logging
import os

import httpx


logger = logging.getLogger(__name__)

NOTIFICATION_SERVICE_BULK_URL = (
    "http://notification-service:8000/notifications/internal/bulk"
)

INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "123")


async def send_bulk_notification(
    user_ids: list[int],
    title: str,
    message: str,
    event_type: str,
):
    if not user_ids:
        logger.info("No users for bulk notification")
        return None

    payload = {
        "user_ids": user_ids,
        "title": title,
        "message": message,
        "event_type": event_type,
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                NOTIFICATION_SERVICE_BULK_URL,
                json=payload,
                headers={
                    "X-Internal-Token": INTERNAL_API_TOKEN,
                },
            )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        logger.warning(
            "Failed to send bulk notification to notification-service: %s",
            exc,
        )
        return None
