# Use Python image
FROM python:3.11-slim

# Add author label
LABEL authors="Adrian Tesula"

# Set working dirctory
WORKDIR /app

# Copy the code inside docker
COPY ./app /app/app
COPY requirements.txt /app/

ENV PYTHONPATH="${PYTHONPATH}:/app"

# Install the dependencies
RUN pip install -r requirements.txt

# Expose default port
EXPOSE 8000

# Default command to run fastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]