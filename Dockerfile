# Use the official Python image as a base
FROM python:3.12.7-slim

# Set environment variables to ensure Python runs in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/
COPY api /app/
COPY donation /app/
COPY eoy_2024_backend /app/
COPY templates /app/
COPY users /app/
COPY manage.py /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend code to the container
COPY . /app/

# Expose the port the application will run on
EXPOSE 8000

# Set the command to run the backend
CMD ["python", "app.py"]
