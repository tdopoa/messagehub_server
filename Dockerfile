# Use Python 3.11 as base image with security updates
FROM python:3.11-slim-bullseye

RUN mkdir -p /app
# Set working directory
WORKDIR /app

COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

ADD . /app
COPY src/ /app/src/

# Copy requirements first to leverage Docker cache

# Sync the project
# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8000"]


