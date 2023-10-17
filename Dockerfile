FROM node:18-alpine3.18


RUN apk add \
    stow \
    vim \
    tmux


EXPOSE 8080


WORKDIR /src
