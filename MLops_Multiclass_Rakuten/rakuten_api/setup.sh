
#!/bin/bash
set -e

# Rakuten API images build only (no docker-compose up here)
echo "[Rakuten API] Building Docker images..."

docker image build app/ -t mon_api_rakuten:latest

docker image build authentication_image/ -t authentication_image:latest

docker image build authorization_image/ -t authorization_image:latest

docker image build prediction_image/ -t prediction_image:latest

echo "[Rakuten API] Images built successfully."
