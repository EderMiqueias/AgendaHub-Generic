import falcon
from pydantic import ValidationError
from typing import List

from app.models.event_model import EventPydantic as Event
from app.services.event_service import EventService


# 1. Recurso para a coleção (/events)
class EventsResource:
    def __init__(self, service: EventService):
        self.service = service

    def on_get(self, req, resp):
        """GET /events"""
        events = self.service.get_events()
        # Falcon (3.0+) serializa automaticamente se atribuir a resp.media
        # Convertendo lista de Pydantic models para lista de dicts
        resp.media = [e.dict() for e in events]
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """POST /events"""
        try:
            # req.media já faz o parse do JSON do corpo
            raw_data = req.get_media()

            # Validação manual do Pydantic
            event_data = Event(**raw_data)

            # Chama o serviço
            created_event = self.service.create_event(event_data)

            resp.media = created_event.dict()
            resp.status = falcon.HTTP_201

        except ValidationError as e:
            # Erro de validação do Pydantic
            raise falcon.HTTPBadRequest(title="Dados inválidos", description=str(e))
        except ValueError as e:
            # Erro de lógica do serviço
            raise falcon.HTTPBadRequest(title="Erro ao criar evento", description=str(e))


# 2. Recurso para item único (/events/{event_id})
class EventItemResource:
    def __init__(self, service: EventService):
        self.service = service

    def on_get(self, req, resp, event_id):
        """GET /events/{id}"""
        try:
            # Falcon passa parâmetros de URL como string por padrão
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

        # Retorna o booleano (True)
        resp.media = deleted
        resp.status = falcon.HTTP_200


# 3. Configuração da Aplicação
def get_app():
    # Instancia o Falcon App
    app = falcon.App()

    # Injeção de dependência manual (Instancia única do serviço)
    event_service = EventService()

    # Instancia os recursos
    events_resource = EventsResource(event_service)
    event_item_resource = EventItemResource(event_service)

    # Define as rotas
    app.add_route('/events', events_resource)
    app.add_route('/events/{event_id}', event_item_resource)

    return app
