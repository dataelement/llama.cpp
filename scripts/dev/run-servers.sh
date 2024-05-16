#!/bin/bash


function run_qwen_72b() {
    model="qwen1_5-72b-chat-q5_k_m.gguf"
    model_dir="/mnt/disks/elem-disk1/workspace/public/llm/Qwen1.5-72B-Chat-GGUF"
    param="-m /models/$model -c 30000 -n 2024 --host 0.0.0.0 --port 8000 --n-gpu-layers 100"
    docker run --name server-ins0 --gpus '"device=0,1"' -itd -v ${model_dir}:/models -p 9300:8000 dataelement/llama.cpp:server-cuda $param
}

function run_cohere() {
    model="ggml-c4ai-command-r-plus-q3_k_m-00001-of-00002.gguf"
    model_dir="/mnt/disks/elem-disk1/workspace/public/llm/c4ai-command-r-plus-iMat.GGUF"
    param="-m /models/$model -c 100000 -n 2048 --host 0.0.0.0 --port 8000 --n-gpu-layers 200"
    docker run --name server-ins1 --gpus '"device=2,3"' -itd -v ${model_dir}:/models -p 9100:8000 dataelement/llama.cpp:server-cuda-0.1 $param
}

# run_qwen_72b
run_cohere