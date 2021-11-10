# set base image (host OS)
FROM python:3.9.5
ENV PYTHONUNBUFFERED=1

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirement.txt /code/

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# copy the content of the local src directory to the working directory
COPY . /code/


CMD ["bash", "./entrypoint.sh"]