# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install necessary dependencies
RUN pip install torch diffusers runpod Pillow

# Command to run the handler when the container starts
CMD ["python", "handler.py"]
