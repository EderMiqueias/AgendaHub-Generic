import falcon
from pydantic import ValidationError

from app.models.event_model import EventPydantic as Event
from app.services.event_service import EventService


class EventsResource:
    def __init__(self, service: EventService):
        self.service = service

    def on_get(self, req, resp):
        """GET /events"""
        events = self.service.get_events()
        resp.media = [e.dict() for e in events]
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """POST /events"""
        try:
            raw_data = req.get_media()
            event_data = Event(**raw_data)

            created_event = self.service.create_event(event_data)

            resp.media = created_event.dict()
            resp.status = falcon.HTTP_201

        except ValidationError as e:
            raise falcon.HTTPBadRequest(title="Dados inválidos", description=str(e))
        except ValueError as e:
            raise falcon.HTTPBadRequest(title="Erro ao criar evento", description=str(e))


class EventItemResource:
    def __init__(self, service: EventService):
        self.service = service

    def on_get(self, req, resp, event_id):
        """GET /events/{id}"""
        try:
            e_id = int(event_id)
        except ValueError:
            raise falcon.HTTPBadRequest(title="ID inválido")

        event = self.service.get_event(e_id)
        if not event:
            raise falcon.HTTPNotFound(title="Evento não encontrado")

        resp.media = event.dict()
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, event_id):
        """DELETE /events/{id}"""
        try:
            e_id = int(event_id)
        except ValueError:
            raise falcon.HTTPBadRequest(title="ID inválido")

        deleted = self.service.delete_event(e_id)
        if not deleted:
            raise falcon.HTTPNotFound(title="Evento não encontrado")

        resp.media = deleted
        resp.status = falcon.HTTP_200


def get_app():
    app = falcon.App()
    event_service = EventService()

    events_resource = EventsResource(event_service)
    event_item_resource = EventItemResource(event_service)

    app.add_route('/events', events_resource)
    app.add_route('/events/{event_id}', event_item_resource)

    return app
