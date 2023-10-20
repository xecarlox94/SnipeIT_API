clear &&\
    docker_build.sh &&\
    docker_run.sh \
        "\
            sh \
        "\
        "\
            -v ${PWD}/src:/src \
            --rm \
            --privileged \
            --name test \
        "\

