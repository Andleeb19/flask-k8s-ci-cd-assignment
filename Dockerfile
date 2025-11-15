# Multi-stage Dockerfile for Flask Application
# Stage 1: Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production stage
FROM python:3.9-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app.py .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]
