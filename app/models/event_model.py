from datetime import datetime
from typing import Union

from pydantic import BaseModel


class Event:
    id: int | None = None
    title: str
    description: str
    event_date: Union[datetime, str]

    def __init__(self, title: str, description: str, date: datetime):
        self.title = title
        self.description = description
        self.date = date


class EventPydantic(BaseModel, Event):
    pass


__all__ = ['Event', 'EventPydantic']
