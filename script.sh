#!/bin/bash

echo "🐝 Setting up DeceptiNet Honeypot System..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p data/logs/{cowrie,dionaea,flask-fake-login}
mkdir -p data/dionaea
mkdir -p honeypots/flask-fake-login
mkdir -p config/cowrie-config

# Set proper permissions
echo "🔐 Setting permissions..."
chmod -R 755 data/
chmod -R 755 config/

# Create the fixed cowrie config
cat > config/cowrie-config/cowrie.cfg << 'EOF'
[honeypot]
hostname = server
log_path = var/log/cowrie
download_path = var/lib/cowrie/downloads
data_path = var/lib/cowrie
contents_path = honeyfs
filesystem_file = share/cowrie/fs.pickle

[output_jsonlog]
logfile = var/log/cowrie/cowrie.json

[output_textlog]
logfile = var/log/cowrie/cowrie.log

[ssh]
listen_endpoints = tcp:2222:interface=0.0.0.0
version = SSH-2.0-OpenSSH_6.0p1 Debian-4+deb7u2

auth_class = AuthRandom
auth_class_parameters = 2, 5, 10

[telnet]
enabled = true
listen_endpoints = tcp:2223:interface=0.0.0.0
EOF

echo "✅ Setup complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Replace your docker-compose.yml with the fixed version"
echo "2. Run: docker-compose down --volumes (to clean old setup)"
echo "3. Run: docker-compose up -d"
echo "4. Test with the testing script"