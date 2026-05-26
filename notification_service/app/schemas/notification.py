from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    user_id: int

    title: str = Field(
        min_length=1,
        max_length=255,
    )

    message: str = Field(
        min_length=1,
        max_length=1000,
    )

    event_type: str = Field(
        min_length=1,
        max_length=100,
    )


class NotificationUpdate(BaseModel):
    is_read: bool


class NotificationRead(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    event_type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InternalNotificationCreate(BaseModel):
    user_id: int
    title: str
    message: str
    event_type: str


class BulkNotificationCreate(BaseModel):
    user_ids: list[int]
    title: str
    message: str
    event_type: str
