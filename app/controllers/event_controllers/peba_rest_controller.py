import pebarest.exceptions
from pebarest import App
from pebarest.models import Resource, Request

from app.models.event_model import EventPydantic as Event
from app.services.event_service import EventService


def get_event_service() -> EventService:
    return EventService()


class EventResource(Resource):
    service = get_event_service()

    def get(self, request: Request, *args, **kwargs):
        return self.service.get_events()

    def post(self, request: Request[Event], *args, **kwargs):
        try:
            return self.service.create_event(request.body)
        except ValueError as e:
            return {"detail": str(e)}, 400


class EventWithParamsResource(Resource):
    service = get_event_service()

    def get(self, request: Request, *args, **kwargs):
        event_id = request.params['event_id']
        return self.service.get_event(event_id)

    def delete(self, request: Request[Event], *args, **kwargs):
        event_id = request.params['event_id']
        deleted = self.service.delete_event(event_id)
        if not deleted:
            raise pebarest.exceptions.NotFoundError(message="Evento não encontrado")
        return deleted


def get_app():
    app = App(__name__)
    app.add_route('/events', EventResource())
    app.add_route('/events/{event_id}', EventResource())
    return app


__all__ = ['get_app']
