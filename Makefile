fmt:
	black src -v --target-version py310

# To avoid import errors, you can configure the PYTHONPATH that pylint will use
pylint:
	pylint --rcfile=".pylintrc" src

run:
	poetry shell & poetry run python src/bazelbot.py
