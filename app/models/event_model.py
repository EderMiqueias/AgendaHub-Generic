from datetime import datetime


class Event:
    id: int | None = None
    title: str
    description: str
    date: datetime

    def __init__(self, title: str, description: str, date: datetime):
        self.title = title
        self.description = description
        self.date = date


__all__ = ['Event']
