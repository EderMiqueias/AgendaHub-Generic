from app.models.event_model import Event
from app.repositories.infrastructure.db.database import Database


class EventRepository:
    _db_service: Database

    def __init__(self, db_service: Database):
        self._db_service = db_service

    def create(self, event: Event) -> Event:
        insert_event_query = """
            INSERT INTO events (title, description, event_date)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        event.id = self._db_service.execute_query(
            insert_event_query, (event.title, event.description, event.event_date)
        )[0]['id']

        return event

    def find_all(self) -> list[Event]:
        return self._db_service.fetch_all("""
            SELECT id, title, description, event_date FROM events
        """)

    def find_by_id(self, event_id: int) -> Event | None:
        return self._db_service.fetch_one("""
            select id, title, description, event_date from events where id = %s
        """, (event_id,))

    def delete(self, event_id: int) -> bool:
        self._db_service.execute_query("""
            DELETE FROM events WHERE id = %s
        """, (event_id,))
        return True
