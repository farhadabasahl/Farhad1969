# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including curl
RUN apt-get update && apt-get install -y gcc curl

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy the wait_for_elasticsearch.sh script
COPY wait_for_elasticsearch.sh /app/

# Make the script executable
RUN chmod +x /app/wait_for_elasticsearch.sh

# Use the script as the entry point
ENTRYPOINT ["/app/wait_for_elasticsearch.sh"]