import os

from fastapi import Header, HTTPException, status


INTERNAL_API_TOKEN = os.getenv(
    "INTERNAL_API_TOKEN",
    "123",
)


async def verify_internal_token(
    x_internal_token: str = Header(..., alias="X-Internal-Token"),
):
    if x_internal_token != INTERNAL_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal token",
        )
