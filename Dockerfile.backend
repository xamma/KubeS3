FROM python:3.11-slim

RUN mkdir /app

COPY /src/requirements.txt /opt/requirements.txt

RUN pip install -r /opt/requirements.txt

COPY /src/main/ /app

WORKDIR /app

EXPOSE 8000

CMD python api.py