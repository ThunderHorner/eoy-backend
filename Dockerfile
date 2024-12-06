# Use the official Python image as a base
FROM python:3.12.7-slim

# Set environment variables to ensure Python runs in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code to the container
COPY api /app/api/
COPY donation /app/donation/
COPY eoy_2024_backend /app/eoy_2024_backend/
COPY templates /app/templates/
COPY users /app/users/
COPY manage.py /app/

# Expose the port the application will run on
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
