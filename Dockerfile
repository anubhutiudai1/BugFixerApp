# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"
ENV FLASK_APP="app.py"
ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"

# Set the working directory in the container
WORKDIR /app

# Install necessary dependencies
RUN pip install Flask google-cloud-aiplatform

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]

# For development, you may use the following CMD instead to enable hot reloading
# CMD ["flask", "run", "--host=0.0.0.0", "--reload"]

# Use a lightweight Nginx image
FROM nginx:alpine

# Copy the HTML file into the Nginx HTML directory
COPY index.html /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Command to start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]
