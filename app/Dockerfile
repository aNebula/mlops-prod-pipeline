# Use a slim, official Python base image for a smaller footprint
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8080

# The command to run the application using Uvicorn, a high-performance ASGI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]