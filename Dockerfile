FROM python:3.13.0a2

ARG DEBIAN_FRONTEND=noninteractive

RUN \
    apt update &&\
    apt install -y \
        stow \
        vim \
        tmux \
        curl \
        jq &&\
    python -m pip install \
        requests \
        python-dotenv \
        flask \
        notion-client


WORKDIR /src


EXPOSE 5000

