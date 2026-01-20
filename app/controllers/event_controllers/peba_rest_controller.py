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


def get_app():
    app = App()
    app.add_route('/events', EventResource())
    return app


__all__ = ['get_app']
