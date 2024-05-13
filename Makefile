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

