# Pull base image
FROM python:3.8

# Set environment variables 
# Python don't write byte code: it won't write .pyc files 
ENV PYTHONDONTWRITEBYTECODE 1

# Python buffered gives familiar output to console
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code 

# Install dependencies
COPY Pipfile /code/

# 'system' flag will avoid pipenv to look for a virtual environment
RUN pip install pipenv

# Install dependencies
RUN pipenv install --skip-lock --system && pipenv install --skip-lock --system --dev

# COPY project 
COPY . /code/