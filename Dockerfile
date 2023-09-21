FROM python:3.10.7-slim

ENV PATH=/root/.poetry/bin:${PATH} \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.6.0 \
    POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update && apt-get -y install --no-install-recommends gcc g++ &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install "poetry==$POETRY_VERSION"

COPY entrypoint.sh pyproject.toml poetry.lock ./

RUN poetry install

COPY server/ ./server

CMD ["./entrypoint.sh"]
