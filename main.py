import os
import uvicorn

framework = os.getenv("APP_FRAMEWORK", "fastapi").lower()

if framework == "fastapi":
    from run_fastapi import app
elif framework == "flask":
    from run_flask import app
else:
    raise RuntimeError(f"Framework inválido: {framework}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
