from datetime import datetime


class Event:
    id: int | None = None
    title: str
    description: str
    date: datetime


__all__ = ['Event']
