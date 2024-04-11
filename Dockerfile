# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc

# Install poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Copying in our source code
COPY ./app /app/app

# Uvicorn will listen on this port
EXPOSE 8000

# Start the app.  Note that we're using `python` here, so if you have
# a script to start your app, it would be something like
# `CMD ["python", "myscript.py"]`
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]