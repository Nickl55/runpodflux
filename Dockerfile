# Use a Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create a directory for the application
WORKDIR /app

# Install necessary dependencies
RUN pip install --no-cache-dir transformers runpod flask

# Copy the handler.py into the container
COPY handler.py /app/

# Expose the port for HTTP server if needed (for local testing)
EXPOSE 8080

# Start the RunPod serverless service
CMD ["python", "handler.py"]
