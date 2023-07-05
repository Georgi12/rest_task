from typing import Optional, Any

from pydantic import BaseModel, Field


class CreateObject(BaseModel):
    id: Optional[int]
    value: Any


class DeleteObject(BaseModel):
    deleted_id: int


class GetObject(BaseModel):
    ids: Optional[list[int]] = Field(default=[])


class ReturnedObject(BaseModel):
    id: int
    value: Any


class ReturnedObjectMany(BaseModel):
    data: list[ReturnedObject]
