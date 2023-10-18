FROM python:3.11.6-alpine3.18

RUN apk add \
    stow \
    vim \
    tmux \
    curl \
    jq

RUN python -m pip install \
    requests \
    python-dotenv \
    notion-client

EXPOSE 8080


WORKDIR /src


RUN echo "\
        ~/.config/.FILES/scripts/.config/scripts/conf/install.sh \
    " > ~/set_config.sh &&\
    chmod +x ~/set_config.sh

