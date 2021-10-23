FROM python:3.7-slim as telegram_bot

ARG REQUIREMENTS_FILE=requirements.txt

COPY ./monika_bot /usr/src/app
COPY ./requirements.txt /usr/src/app

WORKDIR /usr/src/app

RUN apt update && \
    pip install --upgrade pip

RUN pip install -r ${REQUIREMENTS_FILE}

WORKDIR /usr/src/app

CMD ["./startup.sh"]
