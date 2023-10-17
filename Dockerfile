FROM python:3.11.6-alpine3.18

RUN apk add \
    stow \
    vim \
    tmux

RUN python -m pip install requests python-dotenv

EXPOSE 8080


WORKDIR /src
