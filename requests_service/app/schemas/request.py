from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class RequestStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    done = "done"
    rejected = "rejected"


class RequestCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)


class RequestUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    status: RequestStatus | None = None


class RequestRead(BaseModel):
    id: int
    title: str
    content: str
    status: RequestStatus
    author_id: int
    created_at: datetime
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
