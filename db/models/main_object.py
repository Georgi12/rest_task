from typing import Any

from db.connection import BaseStorage


class MainObject(BaseStorage):
    value: Any
