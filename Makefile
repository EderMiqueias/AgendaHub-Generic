install:
	pip install -r requirements.txt

fastapi-local:
	uvicorn run_fastapi:app --reload

flask-local:
	uvicorn run_flask:app --reload

fastapi-docker:
	docker compose --profile fastapi up --build --remove-orphans

flask-docker:
	docker compose --profile flask up --build --remove-orphans
