FROM python:3.13.0a2

ARG DEBIAN_FRONTEND=noninteractive


WORKDIR /src



RUN \
    apt update &&\
    apt install -y \
        stow \
        vim \
        tmux \
        curl \
        jq


#RUN pip3 install -r requirements.txt
RUN \
    pip3 install \
        requests \
        python-dotenv \
        flask \
        notion-client


EXPOSE 5000

