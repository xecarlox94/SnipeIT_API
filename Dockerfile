FROM python:3.11.6-alpine3.18


ARG BUILD_ENV=prod
ENV RUN_ENV=
RUN export BUILD_ENV=


RUN \
    apk add \
        stow \
        vim \
        tmux \
        curl \
        jq &&\
    python -m pip install \
        requests \
        python-dotenv \
        flask \
        notion-client &&\
    echo "\
            ~/.config/.FILES/scripts/.config/scripts/conf/install.sh \
        " > ~/set_config.sh &&\
        chmod +x ~/set_config.sh &&\
    echo "~/set_config.sh" > ~/.bashrc


WORKDIR /src


EXPOSE 5000

