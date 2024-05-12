# pull official base image
FROM python:3.11-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set working directory
WORKDIR /usr/src/app

# update system dependencies
RUN apt-get update && apt-get clean

# add app
COPY . .

# add recipe data (to /usr/src)
COPY ../recipes /usr/src/recipes

# install python dependencies
RUN pip install -r requirements.txt