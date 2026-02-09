install:
	pip install -r requirements.txt

upgrade_pebarest:
	pip uninstall pebarest -y & pip install git+https://github.com/EderMiqueias/PebaREST.git@master

fastapi-local:
	uvicorn run_fastapi:app --reload

flask-local:
	uvicorn run_flask:app --reload

falcon-local:
	gunicorn run_falcon:app --reload

pebarest-local:
	uvicorn run_pebarest:app --reload

fastapi-docker:
	docker compose --profile fastapi up --build --remove-orphans

flask-docker:
	docker compose --profile flask up --build --remove-orphans

falcon-docker:
	docker compose --profile falcon up --build --remove-orphans

pebarest-docker:
	docker compose --profile pebarest up --build --remove-orphans
