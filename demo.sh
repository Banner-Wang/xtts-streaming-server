#!/bin/bash

# 需要外部传入num参数以控制端口和进程的数量
if [ -z "$1" ]; then
  echo "Usage: $0 <num>"
  exit 1
fi

num=$1
base_port=9000

# 简单的检查输入是否为数字
if ! [[ "$num" =~ ^[0-9]+$ ]]; then
    echo "Error: num must be an integer."
    exit 1
fi

# 检查端口在允许范围内（这里假设1024到65535）
if ((base_port + num - 1 > 65535)); then
    echo "Error: Port number exceeds allowed range."
    exit 1
fi

# 定义服务器目录和脚本目录
server_dir="/data/AI_VOICE_WORKSPACE/tts/banner/xtts-streaming-server/server"
script_dir="/data/AI_VOICE_WORKSPACE/tts/banner/xtts-streaming-server"

cd "$server_dir"
# 循环执行启动操作
for ((i=0; i<num; i++)); do
    # 计算当前端口
    port=$(($base_port + $i))

    # 检查端口是否已被占用
    if lsof -i:$port -t >/dev/null; then
        echo "Error: Port $port is already in use."
        continue
    fi

    # 启动Uvicorn服务
    echo "Starting Uvicorn server on port $port..."
    nohup uvicorn main:app --host 0.0.0.0 --port $port &
    sleep 2
done

sleep 60


cd "$script_dir"
for ((i=0; i<num; i++)); do
    # 计算当前端口
    port=$(($base_port + $i))

    # 启动demo.py
    echo "Starting demo.py with port $port..."
    nohup python3 demo.py --port $port > "log_${port}.txt" &
done
echo "All processes started."