# Use Python 3.11 as base image with security updates
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

COPY requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY .env /app/.env

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh


# Set the entrypoint to the script
ENTRYPOINT ["/app/entrypoint.sh"]

