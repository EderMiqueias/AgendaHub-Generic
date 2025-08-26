from app.models.event_model import Event
from app.repositories.event_repository import EventRepository


class EventService:
    def __init__(self):
        self.repository = EventRepository()

    def create_event(self, event: Event) -> Event:
        if not event.title:
            raise ValueError("O título é obrigatório")
        return self.repository.save(event)

    def get_events(self) -> list[Event]:
        return self.repository.find_all()

    def get_event(self, event_id: int) -> Event | None:
        return self.repository.find_by_id(event_id)

    def delete_event(self, event_id: int) -> bool:
        return self.repository.delete(event_id)
