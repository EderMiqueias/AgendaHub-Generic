from app.controllers import app_flask
from asgiref.wsgi import WsgiToAsgi

app = app_flask()
asgi_app = WsgiToAsgi(app)
