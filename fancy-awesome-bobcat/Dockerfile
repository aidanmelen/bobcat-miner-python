ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}

ENV PORT=80
EXPOSE 80

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./src/app /app
WORKDIR /app

ENV FLASK_APP /app/server.py

COPY entrypoint.sh /entrypoint.sh
RUN chmod 0777 /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
