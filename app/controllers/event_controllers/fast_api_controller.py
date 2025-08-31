from fastapi import APIRouter, Depends, HTTPException, FastAPI

from typing import List
from app.models.event_model import EventPydantic as Event
from app.services.event_service import EventService


router = APIRouter(prefix="/events", tags=["Events"])


def get_event_service() -> EventService:
    return EventService()


@router.post("/", response_model=Event)
def create_event(event: Event, service: EventService = Depends(get_event_service)):
    try:
        return service.create_event(event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[Event])
def get_events(service: EventService = Depends(get_event_service)):
    return service.get_events()


@router.get("/{event_id}", response_model=Event)
def get_event(event_id: int, service: EventService = Depends(get_event_service)):
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return event


@router.delete("/{event_id}", response_model=bool)
def delete_event(event_id: int, service: EventService = Depends(get_event_service)):
    deleted = service.delete_event(event_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return deleted


def get_app():
    app = FastAPI()
    app.include_router(router)
    return app


__all__ = ['get_app']
