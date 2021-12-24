FROM python:3.9-alpine

COPY requirements.txt /requirements.txt 

RUN pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh

COPY src/app /app

WORKDIR /app

ENTRYPOINT ["/bin/sh"]

CMD ["/entrypoint.sh"]
