#!/bin/bash

echo "🐝 Setting up DeceptiNet Honeypot System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

print_status "Creating directory structure..."
# Create directory structure
mkdir -p data/logs/{cowrie,dionaea,flask-fake-login}
mkdir -p data/dionaea
mkdir -p honeypots/flask-fake-login
mkdir -p config/{cowrie-config,logstash}

print_status "Setting permissions..."
# Set proper permissions
chmod -R 755 data/
chmod -R 755 config/
chmod -R 755 honeypots/

# Create requirements.txt for Flask app
print_status "Creating Flask requirements.txt..."
cat > honeypots/flask-fake-login/requirements.txt << 'EOF'
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
itsdangerous==2.1.2
click==8.1.7
MarkupSafe==2.1.3
requests==2.31.0
EOF

# Create improved Flask Dockerfile
print_status "Creating Flask Doctorate..."
cat > honeypots/flask-fake-login/Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory with proper permissions
RUN mkdir -p /app/logs && chmod 755 /app/logs

# Copy the Python app
COPY app.py /app/

# Create a non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000', timeout=5)" || exit 1

# Run the application
CMD ["python", "/app/app.py"]
EOF

# Create the fixed cowrie config
print_status "Creating Cowrie configuration..."
cat > config/cowrie-config/cowrie.cfg << 'EOF'
# Cowrie Honeypot Configuration

[honeypot]
hostname = ubuntu-server
log_path = var/log/cowrie
download_path = var/lib/cowrie/downloads
data_path = var/lib/cowrie
contents_path = honeyfs
filesystem_file = share/cowrie/fs.pickle
sessions_path = var/lib/cowrie/sessions
txtcmds_path = share/cowrie/txtcmds

# SSH Configuration
[ssh]
listen_endpoints = tcp:2222:interface=0.0.0.0
version = SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2

# Authentication - allow some logins to succeed for better interaction
auth_class = AuthRandom
auth_class_parameters = 2, 5, 10

# Enable Telnet
[telnet]
enabled = true
listen_endpoints = tcp:2223:interface=0.0.0.0

# Output plugins
[output_jsonlog]
logfile = var/log/cowrie/cowrie.json

[output_textlog]
logfile = var/log/cowrie/cowrie.log

# Enable more realistic shell behavior
[shell]
processes = share/cowrie/cmdoutput.json

# Filesystem
[fs]
contents_path = honeyfs
EOF

# Create basic logstash config (optional)
print_status "Creating Logstash configuration..."
cat > config/logstash/logstash.conf << 'EOF'
input {
  file {
    path => "/var/log/honeypots/cowrie/cowrie.json"
    start_position => "beginning"
    codec => "json"
    type => "cowrie"
  }
  file {
    path => "/var/log/honeypots/flask-fake-login/login.json"
    start_position => "beginning"
    codec => "json"
    type => "flask"
  }
}

filter {
  if [type] == "cowrie" {
    mutate {
      add_field => { "honeypot_type" => "ssh" }
    }
  }
  if [type] == "flask" {
    mutate {
      add_field => { "honeypot_type" => "web" }
    }
  }
}

output {
  stdout {
    codec => rubydebug
  }
  file {
    path => "/var/log/honeypots/aggregated.log"
    codec => "json"
  }
}
EOF

# Copy the existing app.py if it exists
if [ -f "honeypots/flask-fake-login/app.py" ]; then
    print_success "Flask app.py already exists, keeping current version"
else
    print_warning "Flask app.py not found. Please ensure it's in honeypots/flask-fake-login/"
fi

print_success "Setup complete!"
echo ""
print_status "🚀 Next steps:"
echo "1. Ensure your app.py is in honeypots/flask-fake-login/"
echo "2. Stop any running containers: docker-compose down --volumes"
echo "3. Build and start: docker-compose up --build -d"
echo "4. Check logs: docker-compose logs -f"
echo "5. Test the services:"
echo "   - Flask Web: http://localhost:5000"
echo "   - SSH Honeypot: ssh -p 2222 root@localhost"
echo "   - FTP: ftp localhost 21"
echo ""
print_status "🔍 Monitor with:"
echo "   python3 analyzer.py"
echo ""
print_status "☁️ For cloud deployment, we'll set up:"
echo "   - AWS/GCP/Azure deployment scripts"
echo "   - Terraform configurations"
echo "   - Centralized logging"
echo "   - Monitoring and alerts"