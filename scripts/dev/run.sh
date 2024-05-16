#!/bin/bash

function prepare() {
    UBUNTU_VERSION=22.04
    # This needs to generally match the container host's environment.
    # CUDA_VERSION=12.4.1
    CUDA_VERSION=12.2.0
    # Target the CUDA build image
    BASE_CUDA_DEV_CONTAINER=nvidia/cuda:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}
    BASE_CUDA_RUN_CONTAINER=nvidia/cuda:${CUDA_VERSION}-runtime-ubuntu${UBUNTU_VERSION}
    # docker pull $BASE_CUDA_DEV_CONTAINER

    # docker run -itd --gpus all --net=host --name llamacpp-dev -v $HOME:$HOME -v /mnt/disks:/mnt/disks $BASE_CUDA_DEV_CONTAINER bash
    # docker exec llamacpp-dev apt update
    # docker exec llamacpp-dev apt install -y cmake ccache

    # docker run -itd --gpus all --net=host --name llamacpp-rt -v $HOME:$HOME -v /mnt/disks:/mnt/disks $BASE_CUDA_DEV_CONTAINER bash
    # docker exec llamacpp-rt mkdir -p /opt/llamacpp/bin

    # docker run -itd --gpus all --net=host --name llamacpp-dev-cu122 -v $HOME:$HOME -v /mnt/disks:/mnt/disks $BASE_CUDA_DEV_CONTAINER bash
    # docker exec llamacpp-dev-cu122 apt update
    # docker exec llamacpp-dev-cu122 apt install -y cmake ccache

    RT_IMAGE="nvidia/cuda:12.2.0-runtime-ubuntu22.04"
    docker run -itd --gpus all --net=host --name llamacpp-rt-cu122 -v $HOME:$HOME -v /mnt/disks:/mnt/disks $BASE_CUDA_DEV_CONTAINER bash
    # docker exec llamacpp-rt-cu122 mkdir -p /opt/llamacpp/bin

}

function commit_image() {
    docker rmi dataelement/bisheng-rt-llamacpp:latest
    docker cp build/bin/server llamacpp-rt:/opt/llamacpp/bin/llamacpp_server
    docker commit -m "llamacpp image" llamacpp-rt dataelement/bisheng-rt-llamacpp:latest
    docker push dataelement/bisheng-rt-llamacpp:latest
}

function commit_image_cu122() {
    docker rmi dataelement/llama.cpp-server-cuda
    docker build -t dataelement/llama.cpp-server-cuda -f Dockerfile.cu122 .
    docker push dataelement/bisheng-rt-llamacpp:cu122-latest
}

function build() {
    mkdir build
    cd build
    # rm -fr CMakeCache.txt  CMakeFiles || echo "escaped"
    cmake .. -DLLAMA_CUBLAS=ON -DCMAKE_CUDA_ARCHITECTURES="61;70;75;80;86;89;90"
    cmake --build . --config Release
}

# prepare
# commit_image
# commit_image_cu122
build