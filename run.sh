clear &&\
    docker_build.sh &&\
    docker_run.sh \
        "\
            bash \
        "\
        "\
            -v ${PWD}/src:/src \
            --rm \
            --name test \
            --net=host\
        "\

            #-p 5000:5000 \
            #python3 main.py \
