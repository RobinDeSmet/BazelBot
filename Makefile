fmt:
	black src -v --target-version py310

pylint:
	pylint --rcfile=".pylintrc" src

test:
	pytest -vv

run:
	poetry shell & poetry run python src/bazelbot.py

reset:
	docker compose down && docker compose up -d

up:
	docker compose up -d

down:
	docker compose down

test-up:
	docker compose -f compose-test.yaml up -d

test-down:
	docker compose -f compose-test.yaml down

test-reset:
	docker compose -f compose-test.yaml down && docker compose -f compose-test.yaml up -d
