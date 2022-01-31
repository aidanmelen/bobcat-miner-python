ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}

ENV PORT=80

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./src/bobcat /bobcat
WORKDIR /bobcat

ENV FLASK_APP /bobcat/server.py

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

EXPOSE 80