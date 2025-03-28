# Start with a base image that has Python and the required libraries
FROM python:3.9-slim

# Set environment variables to avoid writing .pyc files and optimize Docker caching
ENV PYTHONUNBUFFERED 1

# Create a directory for the application code
WORKDIR /app

# Copy the handler.py file and other necessary files
COPY handler.py /app/

# Install dependencies
RUN pip install --no-cache-dir transformers flask

# Expose port for the Flask server
EXPOSE 8080

# Command to run the handler script with Flask
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]
