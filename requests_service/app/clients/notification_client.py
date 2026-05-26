import logging

import httpx


logger = logging.getLogger(__name__)

NOTIFICATION_SERVICE_URL = (
    "http://notification-service:8000/notifications/internal"
)


async def send_notification(
    user_id: int,
    title: str,
    message: str,
    event_type: str,
):
    payload = {
        "user_id": user_id,
        "title": title,
        "message": message,
        "event_type": event_type,
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                NOTIFICATION_SERVICE_URL,
                json=payload,
            )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        logger.warning(
            "Failed to send notification to notification-service: %s",
            exc,
        )
        return None
