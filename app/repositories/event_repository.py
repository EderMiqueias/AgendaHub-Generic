from app.models.event_model import Event


class EventRepository:
    def save(self, event: Event) -> Event:
        event.id = len(_fake_db) + 1
        _fake_db.append(event)
        return event

    def find_all(self) -> list[Event]:
        return _fake_db

    def find_by_id(self, event_id: int) -> Event | None:
        return next((e for e in _fake_db if e.id == event_id), None)

    def delete(self, event_id: int) -> bool:
        global _fake_db
        before = len(_fake_db)
        _fake_db = [e for e in _fake_db if e.id != event_id]
        return len(_fake_db) < before
