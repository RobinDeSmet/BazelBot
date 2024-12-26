# Stage 0: base image for bazelbot
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION} as base

ENV PYTHONUNBUFFERED=1 \
    PATH=/opt/poetry/bin:$PATH \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    HOME=/home/
ENV VIRTUAL_ENV="${HOME}/.venv"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 - --version 1.8.5 && \
    groupadd -g 1234 appuser && \
    useradd -m -u 1234 -g appuser appuser && \
    mkdir -p ${HOME}

WORKDIR ${HOME}

ENV PYTHONPATH="${HOME}/src:${PYTHONPATH}"

# Stage 1: build image
# Install all runtime dependencies,
# but without project's sources, which get copied later
FROM base as build
COPY pyproject.toml poetry.lock ${HOME}
COPY . ${HOME}
RUN poetry install --no-root --only main && rm -rf ${POETRY_CACHE_DIR}

# Set the .env files
ENV $(cat .env)

USER appuser

EXPOSE 8000

CMD poetry run python src/bazelbot.py