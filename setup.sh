#!/bin/bash

echo "Honeypot Setup"
echo "========================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

# Create directory structure
echo "Creating directories..."
mkdir -p logs/web
mkdir -p logs/ssh
# Make scripts executable
chmod +x analyze.py

echo "Setup complete!"
echo ""
echo "To start the honeypots:"
echo "   docker-compose up -d"
echo ""
echo "To test:"
echo "   Web: http://localhost:8080"
echo "   SSH: ssh -p 2222 root@localhost"
echo ""
echo "To analyze logs:"
echo "   python3 analyze.py"
echo ""
echo "To stop:"
echo "   docker-compose down"