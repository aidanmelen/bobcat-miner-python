FROM python:3.7-slim

RUN pip install poetry

COPY . /bobcat_miner_python

WORKDIR bobcat_miner_python

RUN poetry install --no-interaction --no-ansi 

ENTRYPOINT ["poetry", "run", "/bin/bash"]
