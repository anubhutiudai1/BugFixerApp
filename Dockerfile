# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS="/BugFixerApp/credentials.json"
ENV TZ=Asia/Kolkata

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Install additional packages
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Configure logging
RUN mkdir -p /var/log/flask
ENV FLASK_LOG_FILE=/var/log/flask/app.log
ENV FLASK_LOG_LEVEL=DEBUG

# Expose the port Flask is running on
EXPOSE 5000

# Run the application
CMD ["python", "server.py"]
