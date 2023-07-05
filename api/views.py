from fastapi import APIRouter, Depends

from api.validators import CreateObject, ReturnedObject, DeleteObject, ReturnedObjectMany, GetObject
from db.models.main_object import MainObject

rest_router = APIRouter()


@rest_router.get("/", response_model=ReturnedObjectMany)
def select(request: GetObject):
    return {"data": MainObject.get(*request.ids)}


@rest_router.delete("/", response_model=ReturnedObject)
def delete(request: DeleteObject):
    return MainObject.delete(**request.dict())


@rest_router.post("/", response_model=ReturnedObject)
def create(request: CreateObject):
    return MainObject.create(request.dict(exclude_none=True))
