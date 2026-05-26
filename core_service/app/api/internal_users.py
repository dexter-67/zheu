from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.internal_security import verify_internal_token
from app.db.database import get_db
from app.repositories.user_repository import get_resident_users


router = APIRouter(
    prefix="/internal/users",
    tags=["internal-users"],
)


@router.get(
    "",
    dependencies=[Depends(verify_internal_token)],
)
async def get_internal_users(
    db: AsyncSession = Depends(get_db),
):
    users = await get_resident_users(db)

    return [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }
        for user in users
    ]
