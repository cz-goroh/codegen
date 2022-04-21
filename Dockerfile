FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    pip install -r requirements.txt
