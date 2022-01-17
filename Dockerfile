ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim

RUN pip install poetry

COPY . /bobcat_miner_python

WORKDIR bobcat_miner_python

RUN poetry install --no-interaction --no-ansi 

ENTRYPOINT ["poetry", "run", "bobcat"]
