fmt:
	black src -v --target-version py310

pylint:
	pylint --rcfile=".pylintrc" src

test:
	pytest -vv -s tests/test_bazelbot.py

test-llm:
	pytest -vv -s tests/test_bazelbot_llm.py

run:
	poetry shell & poetry run python src/bazelbot.py

reset:
	docker compose down && docker compose up -d

up:
	docker compose up -d

down:
	docker compose down