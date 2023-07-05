from __future__ import annotations

from copy import deepcopy
from enum import Enum, StrEnum
from time import sleep

from pydantic import BaseModel

from errors.errors import UserWrongDbSaveError, DeleteNotExistsObjectError


class InitialId(Enum):
    ONE: int = 1


class FieldName(StrEnum):
    ID_FIELD = 'id'


class BaseStorage(BaseModel):

    id: int
    __storage: dict = {}
    __last_id: dict = {}
    __back_up: dict = {}

    __in_transaction = False
    __operations_history: list[dict] = []

    @classmethod
    def wait_transaction(cls, **kwargs):
        in_transaction = kwargs.get('in_transaction', False)
        if cls.__in_transaction and not in_transaction:
            while cls.__in_transaction:
                sleep(1)

    @classmethod
    def create(cls, value: dict, **kwargs) -> BaseStorage:
        cls.wait_transaction(**kwargs)
        cls.__last_id.setdefault(cls.__name__, 0)
        cls.__storage.setdefault(cls.__name__, {})
        if FieldName.ID_FIELD.value not in value:

            cls.__last_id[cls.__name__] += 1
            cls.__storage[cls.__name__][cls.__last_id[cls.__name__]] = {
                FieldName.ID_FIELD.value: cls.__last_id[cls.__name__], **value
            }
            if cls.__in_transaction:
                cls.__operations_history.append({
                    "name": "create",
                    "cancel": cls.delete,
                    "cancel_params": {"deleted_id": cls.__last_id[cls.__name__]}
                })
            return cls(**cls.__storage[cls.__name__][cls.__last_id[cls.__name__]])

        new_id = value[FieldName.ID_FIELD.value]
        if new_id in cls.__storage[cls.__name__]:
            raise UserWrongDbSaveError(f'Object with id {new_id} already exists')
        cls.__storage[cls.__name__][new_id] = value
        if cls.__last_id[cls.__name__] < new_id:
            cls.__last_id[cls.__name__] = new_id

        if cls.__in_transaction:
            cls.__operations_history.append({
                "name": "create",
                "cancel": cls.delete,
                "cancel_params": {"deleted_id": new_id}
            })
        return cls(**cls.__storage[cls.__name__][new_id])

    @classmethod
    def delete(cls, deleted_id: int, **kwargs) -> BaseStorage | None:
        cls.wait_transaction(**kwargs)
        if deleted_id not in cls.__storage.get(cls.__name__, []):
            raise DeleteNotExistsObjectError(f'Object with id {deleted_id} is not exists for model {cls.__name__}')
        deleted_object = cls(**cls.__storage[cls.__name__].pop(deleted_id))
        if cls.__in_transaction:
            cls.__operations_history.append({
                "name": "delete",
                "cancel": cls.create,
                "cancel_params": deleted_object.dict()
            })
        return deleted_object

    @classmethod
    def get(cls, *ids, **kwargs) -> list[BaseStorage]:
        cls.wait_transaction(**kwargs)
        if not ids:
            return [cls(**cls.__storage[cls.__name__][i]) for i in cls.__storage.get(cls.__name__, {})]
        return [cls(**cls.__storage[cls.__name__][i]) for i in cls.__storage.get(cls.__name__, {}) if i in ids]

    @classmethod
    def start_transaction(cls):
        cls.in_transaction = True
        cls._create_backup()

    @classmethod
    def end_transaction(cls):
        cls.__back_up = {}
        cls.__operations_history = []
        cls.in_transaction = False

    @classmethod
    def _create_backup(cls):
        cls.__back_up = deepcopy(cls.__storage)

    @classmethod
    def failed_transaction(cls):
        cls.__storage = deepcopy(cls.__back_up)

    @classmethod
    def cancel_operations(cls, operations_count):
        for tick in range(operations_count):
            operation = cls.__operations_history.pop()
            operation['cancel'](operation['cancel_params'])



