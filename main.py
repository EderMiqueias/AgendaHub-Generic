import os
from wsgiref.simple_server import make_server

import uvicorn


framework = os.getenv("APP_FRAMEWORK", "pebarest").lower()

if framework == "fastapi":
    from run_fastapi import app
elif framework == "flask":
    from run_flask import asgi_app as app
elif framework == "pebarest":
    from run_pebarest import app
    with make_server('', 8000, app) as httpd:
        print("Server listening on http://127.0.0.1:8000")
        httpd.serve_forever()
else:
    raise RuntimeError(f"Framework inválido: {framework}")


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
