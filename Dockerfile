FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directories for Django
RUN mkdir -p /app/logs /app/static /app/media

# Make port 8000 available
EXPOSE 8000

# Set up proper permissions
RUN chmod +x /app/manage.py

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]