FROM python:3.9-slim

COPY requirements.txt /requirements.txt 

RUN pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh

COPY src/bobcat /bobcat
COPY tests /bobcat

ENTRYPOINT ["/bin/bash"]

CMD ["/entrypoint.sh"]
