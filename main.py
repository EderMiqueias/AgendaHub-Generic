import os
from wsgiref.simple_server import make_server

import uvicorn


framework = os.getenv("APP_FRAMEWORK", "pebarest").lower()


if __name__ == "__main__":
    if framework == "fastapi":
        from run_fastapi import app
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    elif framework == "flask":
        from run_flask import asgi_app as app
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    elif framework == "falcon":
        from run_falcon import get_app

        app = get_app()
        print("Falcon Server (WSGI) listening on http://127.0.0.1:8000")

        with make_server('', 8000, app) as httpd:
            httpd.serve_forever()
    elif framework == "pebarest":
        from run_pebarest import app

        # Generate tests for the application
        print("Creating tests for application...")
        app.generate_tests({
            '/greeting': {
                'GET': None,
                'POST': {
                    "title": "School Meeting",
                    "description": "Meeting to discuss the school schedule",
                    "event_date": "2023-10-01T14:00:00Z"
                }
            }
        }, output_file="tests/test_events_api.py")

        with make_server('', 8000, app) as httpd:
            print("Server listening on http://127.0.0.1:8000")
            httpd.serve_forever()
    else:
        raise RuntimeError(f"Framework inválido: {framework}")
