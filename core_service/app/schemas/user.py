from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    resident = "resident"
    admin = "admin"


class UserRead(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str
