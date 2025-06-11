# Create this file: ./honeypots/flask-fake-login/Dockerfile

FROM python:3.9-slim

WORKDIR /flask-fake-login

# Install Flask
RUN pip install flask

# Create logs directory
RUN mkdir -p /app/logs

# Copy the Python app
COPY app.py /app/

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]