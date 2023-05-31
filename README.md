# DocManageSystem Backend Docker Image

This Docker image allows you to run the DocManageSystem backend application in a containerized environment using Python 3.11 on Alpine Linux.

## Prerequisites

- Docker installed on your system

## Usage

1. Build the Docker image:
   ```bash
   docker build -t backend .
   ```
2. Run the Docker container:
   ```bash
   docker run \
    --name backend \
    --restart=always \
    -v DocManageSystem_backend:/app/DocManageSystem/store \
    -p 8000:8000 \
    -d \
    backend
   ```
3. Clear database and files
    ```bash
    docker exec backend ./deploy.sh delete
    ```

## Configuration
The application can be configured using environment variables. You can provide your own .env file with the required settings. To get started, you can rename the provided .env.example file to .env and modify the values as needed.
