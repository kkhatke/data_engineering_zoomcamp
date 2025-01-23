# Docker through cli 

- Run hello-world image

`docker run hello-world`

It will go to docker hub and download the image and run it

- Run in interactive mode

`docker run -it hello-world bash`

-it = interactive mode
bash = executable inside the container which will run bash shell

- Run specific version

`docker run -it python:3.8`
-It will run python image with version 3.8 in python shell

- Run python image specific entry point

`docker run -it --entrypoint=bash python:3.8`
-entrypoint = to specify the entry point of the image

# Docker File

FROM image:tag
RUN command
WORKDIR container_path
COPY source_path destination_path
ENTRYPOINT ["executable"]

# Example
FROM python:3.8
RUN pip install pandas
WORKDIR /app
COPY xyz.py xyz.py
ENTRYPOINT ["bash"]

-- It will pull the image of python:3.8 from docker hub then run the command in the container and create a working directory in the container and copy the file xyz.py to the working directory.

If we want to change the entry point of the image then we can use ENTRYPOINT ["executable"], 
for example if we want to run pipeline.py in python shell then we can use ENTRYPOINT ["python", "pipeline.py"]

# Build Docker Image

`docker build -t myimage_name:tag .`

-It will build the image from the current directory

# Run Docker Image

`docker run -it myimage_name:tag`

# Passing Arguments to Docker Image

`docker run -it myimage_name:tag arg1 arg2 arg3`

-It will run the image and pass the arguments

# Remove Container

`docker rm -f container_id1 container_id2`

-It will remove the container, add -f to force remove, add --all to remove all the containers, add container_id's to remove specific containers

# Remove Image

`docker rmi -f image_id1 image_id2`

-It will remove the image, add -f to force remove, add --all to remove all the images, add image_id's to remove specific images


