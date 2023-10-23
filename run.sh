clear &&\
    docker_build.sh &&\
    docker_run.sh \
        "\
            python3 main.py \
        "\
        "\
            -v ${PWD}/src:/src \
            --rm \
            --name test \
            -p 5000:5000 \
            --net=host\
        "\

