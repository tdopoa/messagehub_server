# Use Python 3.11 as base image with security updates
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Update system packages and install security updates
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "message_hub_server_api.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
