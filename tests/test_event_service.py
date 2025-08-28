import pytest
from datetime import datetime

from app.repositories.event_repository import EventRepository
from app.repositories.infrastructure.db.db_postgres import PostgresDB
from app.services.event_service import EventService
from app.models.event_model import Event


@pytest.fixture
def service():
    """
    Fixture to provide an EventService with a fake repository.
    """
    repo = EventRepository(PostgresDB())
    return EventService(repo)


def test_create_event_success(service):
    """
    Test creating an event successfully.
    """
    event = Event(title="Show", description="Show de rock", date=datetime.now())
    saved_event = service.create_event(event)

    assert saved_event.id == 1
    assert saved_event.title == "Show"


def test_create_event_without_title_raises_error(service):
    """
    Test creating an event without a title raises a ValueError.
    """
    event = Event(title="", description="Evento sem título", date=datetime.now())

    with pytest.raises(ValueError) as exc:
        service.create_event(event)

    assert str(exc.value) == "O título é obrigatório"


def test_get_events(service):
    """
    Test retrieving all events.
    """
    service.create_event(Event(title="A", description="desc", date=datetime.now()))
    service.create_event(Event(title="B", description="desc", date=datetime.now()))

    events = service.get_events()

    assert len(events) >= 2


def test_get_event_by_id(service):
    """
    Test retrieving an event by its ID.
    """
    event = service.create_event(Event(title="Teste", description="desc", date=datetime.now()))

    found = service.get_event(event.id)

    assert found is not None
    assert found.id == event.id
    assert found.title == "Teste"


def test_get_event_not_found(service):
    """
    Test retrieving a non-existent event returns None.
    """
    found = service.get_event(999)
    assert found is None


def test_delete_event_success(service):
    """
    Test deleting an event successfully.
    """
    event = service.create_event(Event(title="Deletar", description="desc", date=datetime.now()))

    result = service.delete_event(event.id)

    assert result is True
    assert service.get_event(event.id) is None


def test_delete_event_not_found(service):
    """
    Test deleting a non-existent event returns False.
    """
    result = service.delete_event(1234)
    assert result is False
