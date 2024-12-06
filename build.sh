#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define variables
CONTAINER_NAME="crypto_tip_backend"
DOCKER_IMAGE="crypto_tip_backend_image"
APP_PORT=8000  # Adjust this if your backend runs on a different port

# Stop and remove the existing container if it's running
if docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q .; then
    echo "Stopping and removing existing container: ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME}
    docker rm ${CONTAINER_NAME}
fi

# Build the Docker image
echo "Building Docker image: ${DOCKER_IMAGE}"
docker build -t ${DOCKER_IMAGE} .

# Run the container
echo "Running the container: ${CONTAINER_NAME}"
docker run -d -p ${APP_PORT}:8000 --name ${CONTAINER_NAME} ${DOCKER_IMAGE}

echo "Deployment complete. Backend is running on port ${APP_PORT}."
