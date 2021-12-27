FROM python:3.9-slim

COPY requirements.txt /requirements.txt 

RUN pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh

COPY src/app /app

WORKDIR /app

ENTRYPOINT ["/bin/bash"]

CMD ["/entrypoint.sh"]
