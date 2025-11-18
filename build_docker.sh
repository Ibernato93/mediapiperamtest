#!/bin/bash
version=$(awk '/version:/ {print $2}' src/mediapipetest/app/version.yaml)

cd src/mediapipetest || exit 1

echo "Version to build: $version"
docker build -f Dockerfile -t mediapipetest:"$version" .
docker run -d -p 5100:5100 \
  --name mediapipetest \
  --add-host=host.docker.internal:host-gateway \
  --restart unless-stopped \
  mediapipetest:"$version"
