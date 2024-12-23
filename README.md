# pyairbyte

This repository contains the source code for the `pyairbyte` project. This guide will help you compile the project and create a Docker image. Additionally, it provides steps to run the Docker image locally.

TODO: Add support for streaming the data from the source

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- [Docker](https://www.docker.com/get-started) (Follow the link for installation instructions)

## Building the Docker Image

1. Clone the repository:

    ```sh
    git clone git@github.com:ashwin-gangadhar-mdb/pyairbyte-svc.git
    cd pyairbyte-svc
    ```

2. Build the Docker image:

    ```sh
    docker build -t pyairbyte-svc:latest .
    ```

    This command will create a Docker image with the tag `pyairbyte-svc:latest`.

## Running the Docker Image Locally

1. Run the Docker container:

    ```sh
    docker run -d --name pyairbyte_container pyairbyte-svc:latest
    ```

    This command will start a new container named `pyairbyte_container` in detached mode.

2. Verify the container is running:

    ```sh
    docker ps
    ```

    You should see `pyairbyte_container` listed in the output.

## Accessing the Application

To access the application, you can use the following `curl` command to interact with the API hosted on `localhost:5000`:

```sh
curl -X POST 'localhost:5000/ab/source' \
--header 'Accept-Encoding: "gzip, deflate"' \
--header 'Keep-Alive: 10000' \
--header 'Content-Type: application/json' \
--data '{
    "source": "source-faker",
    "config": {"count": 10000},
    "streams": "products"
}'
```

This command sends a POST request to the `/ab/source` endpoint with the specified headers and JSON data.

## Stopping and Removing the Container

To stop the running container, use:

```sh
docker stop pyairbyte_container
```

To remove the container, use:

```sh
docker rm pyairbyte_container
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/get-started/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/docker/)

Feel free to reach out if you have any questions or need further assistance.
