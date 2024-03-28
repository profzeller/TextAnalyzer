# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project files to the container
COPY . /app/

# Copy the entrypoint script
COPY entrypoint.sh /app/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint script to run when the container starts
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the application
CMD ["gunicorn", "textanalyzer.wsgi:application", "--bind", "0.0.0.0:8000"]
