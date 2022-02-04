ARG PYTHON_VERSION=3.10
ARG POETRY_VERSION=1.1.4

FROM python:${PYTHON_VERSION} as base
RUN pip install --upgrade pip \
 && pip install poetry${POETRY_VERSION+==$POETRY_VERSION}
WORKDIR /app
COPY pyproject.toml *poetry.lock .
RUN poetry install --no-interaction --no-ansi --no-root
RUN mkdir /var/log/bobcat && mkdir /etc/bobcat
ENTRYPOINT ["poetry", "run"]
CMD ["bash"]

FROM base as dev
COPY . .
RUN poetry install --no-interaction --no-ansi
RUN apt-get update && apt-get install -y curl jq vim.tiny \
 && ln -s /usr/bin/vim.tiny /usr/bin/vim

FROM dev as test
ENTRYPOINT ["poetry", "run"]
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]

FROM test AS build
RUN poetry build --format wheel

# package up tiny release image
FROM python:${PYTHON_VERSION}-alpine AS release
COPY --from=build /app/dist /app/dist
RUN mkdir /var/log/bobcat && mkdir /etc/bobcat \
 && pip install /app/dist/*.whl
ENTRYPOINT ["bobcat"]