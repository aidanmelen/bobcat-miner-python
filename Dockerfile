FROM python:3.9-slim

RUN pip install poetry
COPY pyproject.toml *poetry.lock .

COPY src/bobcat_miner /bobcat_miner
COPY tests /bobcat_miner

RUN poetry install --no-interaction --no-ansi --no-root

ENTRYPOINT ["poetry", "run", "bobcat-autopilot"]

CMD ["/entrypoint.sh"]
