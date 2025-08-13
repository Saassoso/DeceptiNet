FROM python:3.9-slim

WORKDIR /app

# Install Flask
RUN pip install flask

# Copy the app
COPY app.py /app/

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]