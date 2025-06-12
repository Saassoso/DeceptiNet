
FROM python:3.9-slim

WORKDIR /app

# Install Flask
RUN pip install flask

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && chmod 755 /app/logs

# Copy the Python app
COPY app.py /app/

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "/app/app.py"]