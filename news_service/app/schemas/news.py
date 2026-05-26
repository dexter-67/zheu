from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class NewsCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    content: str = Field(min_length=1)
    is_published: bool = True


class NewsUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=200)
    content: str | None = Field(default=None, min_length=1)
    is_published: bool | None = None


class NewsRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    updated_at: datetime | None
    is_published: bool

    model_config = ConfigDict(from_attributes=True)
