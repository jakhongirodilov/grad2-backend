# Use the official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first (for efficient caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy .env file (ensure it's included in .dockerignore if sensitive)
COPY .env .env

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port Gunicorn will run on
EXPOSE 8000

# Start the Gunicorn server
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
