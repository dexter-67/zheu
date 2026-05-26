from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    user_data: UserCreate,
    hashed_password: str,
) -> User:
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_id(
    db: AsyncSession,
    user_id: int,
) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )

    return result.scalar_one_or_none()


async def get_resident_users(
    db: AsyncSession,
):
    result = await db.execute(
        select(User).where(User.role == "resident")
    )

    return result.scalars().all()
