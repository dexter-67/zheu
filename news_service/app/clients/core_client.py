import logging
import os

import httpx


logger = logging.getLogger(__name__)

CORE_SERVICE_USERS_URL = (
    "http://core-service:8000/internal/users"
)

INTERNAL_API_TOKEN = os.getenv("INTERNAL_API_TOKEN", "123")


async def get_resident_users() -> list[dict]:
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                CORE_SERVICE_USERS_URL,
                headers={
                    "X-Internal-Token": INTERNAL_API_TOKEN,
                },
            )

            response.raise_for_status()
            return response.json()

    except httpx.HTTPError as exc:
        logger.warning(
            "Failed to get users from core-service: %s",
            exc,
        )
        return []
