# pull official base image
FROM python:3.11-slim-buster

# set working directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

# add app
COPY . .

# install python dependencies
RUN pip install -r requirements.txt

