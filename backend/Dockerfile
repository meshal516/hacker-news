# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app


# Install Python dependencies
# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Collect static files (if you have any and serve them with Django/whitenoise)
# Ensure STATIC_ROOT is set in settings.py if you uncomment this
# RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run gunicorn with Uvicorn workers for an ASGI application
# Ensure 'asgi:application' correctly points to your ASGI application instance
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "asgi:application", "-k", "uvicorn.workers.UvicornWorker"] 