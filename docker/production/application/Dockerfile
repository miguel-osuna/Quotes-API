# Pull base image
FROM python:3.11.3-slim-buster

# Set environment variables 
# Python don't write byte code: it won't write .pyc files 
ENV PYTHONDONTWRITEBYTECODE 1

# Python buffered gives familiar output to console
ENV PYTHONUNBUFFERED 1

# Update container dependencies
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \ 
    && rm -rf /usr/share/doc \ 
    && rm -rf /usr/share/man

# Set work directory
WORKDIR /app 

# Copy dependency files
COPY Pipfile Pipfile.lock /app/

# Install Pipenv
RUN pip install --upgrade pip
RUN pip install pipenv

# Install dependencies
RUN pipenv install --ignore-pipfile --system && pipenv install --ignore-pipfile --dev --system

# Copy start bash script ahd change permissions
COPY ./docker/production/application/start /start
RUN sed -i 's/\r$//g' /start 
RUN chmod +x /start 

# COPY project 
COPY . /app/