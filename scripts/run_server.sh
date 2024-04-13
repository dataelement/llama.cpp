#!/bin/bash


function run_qwen() {
    export CUDA_VISIBLE_DEVICES=1
    model="/mnt/disks/elem-disk1/workspace/public/llm/Qwen1.5-32B-Chat-GGUF/qwen1_5-32b-chat-q5_k_m.gguf"
    ./build/bin/server -m $model -c 30000 -n 2024 --host 0.0.0.0 --port 9301 --n-gpu-layers 100
}

function run_cohere() {
    export CUDA_VISIBLE_DEVICES=2
    model="/opt/bisheng-rt/models/model_repository/command-r-gguf/c4ai-command-r-v01-Q5_K_M.gguf"
   ./build/bin/server -m $model -c 60000 -n 2048 --host 0.0.0.0 --port 9100 --n-gpu-layers 100 --chat-template cohere
}

run_qwen