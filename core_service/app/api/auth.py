from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.user import UserCreate, UserRead, UserLogin, TokenResponse, RefreshTokenRequest
from app.services.auth_service import register_user, login_user, refresh_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await register_user(db=db, user_data=user_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    return await login_user(db=db, user_data=user_data)


@router.post("/refresh", response_model=TokenResponse)
async def refesh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    return await refresh_access_token(db=db, refresh_token=token_data.refresh_token)
