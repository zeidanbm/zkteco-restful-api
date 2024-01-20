# Zkteco Restful API

## Build the Docker Image:
Open a terminal, navigate to the directory containing the Dockerfile, and run the following command to build the Docker image:
```
docker build -t zkteco-restful-api-image .
```

## Run the Docker Container:
After successfully building the image, you can run a container from it:
```
docker run -p 4000:80 --restart always zkteco-restful-api-image
```

## Bypass authorization on re-running subprocess
`<your_username>` ALL=(ALL) NOPASSWD: /usr/sbin/service `<service_name>`