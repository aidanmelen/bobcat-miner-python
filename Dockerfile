FROM python:3.9-slim

RUN pip install poetry

COPY . /bobcat_miner_python

WORKDIR bobcat_miner_python

RUN poetry install --no-interaction --no-ansi

ENTRYPOINT ["poetry", "run", "bobcat-autopilot"]

CMD ["/entrypoint.sh"]
