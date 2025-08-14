FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies and Flask
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir flask

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash honeypot

# Copy the application
COPY app.py /app/

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && \
    chown -R honeypot:honeypot /app

# Switch to non-root user
USER honeypot

# Health check to ensure the service is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Expose port
EXPOSE 5000

# Set environment variables for production
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "app.py"]