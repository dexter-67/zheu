from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)
from app.schemas.user import UserCreate, UserLogin
from app.repositories.user_repository import get_user_by_id


async def register_user(db: AsyncSession, user_data: UserCreate):
    existing_email_user = await get_user_by_email(db, user_data.email)

    if existing_email_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    existing_username_user = await get_user_by_username(db, user_data.username)

    if existing_username_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким username уже существует",
        )

    hashed_password = hash_password(user_data.password)

    return await create_user(
        db=db,
        user_data=user_data,
        hashed_password=hashed_password,
    )


async def login_user(db: AsyncSession, user_data: UserLogin):
    user = await get_user_by_email(db, user_data.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "type": "access",
        }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": str(user.id),
            "type": "refresh",
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def refresh_access_token(db: AsyncSession, refresh_token: str):
    payload = decode_token(refresh_token)

    token_type = payload.get("type")

    if token_type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Передан не refresh token",
        )

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный refresh token",
        )

    user = await get_user_by_id(db, int(user_id))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "type": "access",
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
