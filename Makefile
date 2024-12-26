test:
	poetry shell & poetry run pytest -s -v -m "not llm"

test-llm:
	poetry shell & poetry run pytest -s -v -m "llm"

run:
	poetry shell & poetry run python src/bazelbot.py

up:
	docker compose up -d

down:
	docker compose down -v

reset:
	docker compose down && docker compose up -d

test-up:
	docker compose -f compose.test.yaml up -d

test-down:
	docker compose -v -f compose.test.yaml down

test-reset:
	docker compose -v -f compose.test.yaml down && docker compose -f compose.test.yaml up -d