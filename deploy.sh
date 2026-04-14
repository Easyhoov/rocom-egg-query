#!/bin/bash
# 洛克王国孵蛋查询 - 部署脚本
SERVER="175.178.176.174"
PORT="2026"
REMOTE_DIR="/root/rocom-egg-query"

echo "📦 Deploying to $SERVER:$PORT ..."

# Copy files
scp -r main.py index.html download_data.py requirements.txt data/ root@$SERVER:$REMOTE_DIR/

# Restart service
ssh root@$SERVER "cd $REMOTE_DIR && pkill -f 'uvicorn main:app' || true; nohup uvicorn main:app --host 0.0.0.0 --port $PORT > server.log 2>&1 &"

echo "✅ Done! Check: http://$SERVER:$PORT/"
