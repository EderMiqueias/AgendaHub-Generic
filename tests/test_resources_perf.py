from datetime import datetime as dt

from app.controllers.event_controllers.falcon_controller import get_app as get_falcon_app, EventsResource as ER_falcon
from app.controllers.event_controllers.peba_rest_controller import get_app as get_peba_rest_app, EventResource as ER_peba
from app.controllers.event_controllers.fast_api_controller import get_app as get_fastapi_app, get_events as get_events_fastapi, create_event as create_event_fastapi
from app.controllers.event_controllers.flask_controller import get_app as get_flask_api_app, get_events as get_events_flask, create_event as create_event_flask

N = 5000

print("\n\nTestando Falcon...")
start = dt.now()
app = get_falcon_app()
for i in range(N):
    app.add_route(f'/events{i}', ER_falcon(object()))
print("Tempo total de execução:", (dt.now() - start).total_seconds(), "segundos")

print("\nTestando Fastapi...")
start = dt.now()
app = get_fastapi_app()
for i in range(N):
    app.add_api_route(f'/events{i}', get_events_fastapi, methods=["GET"])
    app.add_api_route(f'/events{i}', create_event_fastapi, methods=["POST"])
print("Tempo total de execução:", (dt.now() - start).total_seconds(), "segundos")

print("\nTestando Flask...")
start = dt.now()
app = get_flask_api_app()
for i in range(N):
    app.add_url_rule(f'/events{i}', endpoint=f'event_{i}_get', view_func=get_events_flask, methods=["GET"])
    app.add_url_rule(f'/events{i}', endpoint=f'event_{i}_post', view_func=create_event_flask, methods=["POST"])
print("Tempo total de execução:", (dt.now() - start).total_seconds(), "segundos")

print("\nTestando PebaREST...")
start = dt.now()
app = get_peba_rest_app()
for i in range(N):
    app.add_route(f'/events{i}', ER_peba())
print("Tempo total de execução:", (dt.now() - start).total_seconds(), "segundos")
