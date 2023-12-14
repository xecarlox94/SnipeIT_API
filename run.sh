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
            -p 5000:5000 \
            --net=host\
        "\

            #python3 main.py \
