from flask import Blueprint, request, jsonify, Flask, abort
from pydantic import ValidationError
from typing import List

from app.models.event_model import EventPydantic as Event
from app.services.event_service import EventService


events_bp = Blueprint('events', __name__, url_prefix='/events')


def get_event_service() -> EventService:
    return EventService()


@events_bp.route("/", methods=["POST"])
def create_event():
    service = get_event_service()
    try:
        data = request.get_json()
        event_in = Event(**data)
        created_event = service.create_event(event_in)
        return jsonify(created_event), 200
    except ValidationError as e:
        return jsonify(e.errors()), 422
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400


@events_bp.route("/", methods=["GET"])
def get_events():
    service = get_event_service()
    events = service.get_events()

    return jsonify(events), 200


@events_bp.route("/<int:event_id>", methods=["GET"])
def get_event(event_id: int):
    service = get_event_service()
    event = service.get_event(event_id)

    if not event:
        return jsonify({"detail": "Evento não encontrado"}), 404

    return jsonify(event), 200


@events_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event(event_id: int):
    service = get_event_service()
    deleted = service.delete_event(event_id)

    if not deleted:
        return jsonify({"detail": "Evento não encontrado"}), 404

    return jsonify(deleted), 200


def get_app():
    app = Flask(__name__)
    app.register_blueprint(events_bp)
    return app


__all__ = ['get_app']