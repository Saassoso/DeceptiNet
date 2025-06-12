#!/bin/bash

echo "🐝 Setting up DeceptiNet Honeypot System..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p data/logs/{cowrie,dionaea,flask-fake-login}
mkdir -p honeypots/{cowrie,flask-fake-login}

# Set proper permissions for log directories
echo "🔐 Setting permissions..."
chmod -R 755 data/logs/

# Create empty log files to test
touch data/logs/cowrie/cowrie.log
touch data/logs/cowrie/cowrie.json
touch data/logs/dionaea/dionaea.log
touch data/logs/flask-fake-login/login.log

echo "📊 Directory structure created:"
tree data/ honeypots/ 2>/dev/null || find data/ honeypots/ -type d

echo ""
echo "🚀 Next steps:"
echo "1. Copy the fixed docker-compose.yml"
echo "2. Copy the fixed Dockerfile to honeypots/flask-fake-login/"
echo "3. Make sure all config files are in place"
echo "4. Run: docker-compose up -d"
echo "5. Test with: docker-compose logs -f"

echo ""
echo "🧪 Test commands after startup:"
echo "- SSH honeypot: ssh -p 2222 root@localhost"
echo "- Web honeypot: curl http://localhost:5000"
echo "- Check logs: tail -f data/logs/*/logs/*"

echo ""
echo "✅ Setup complete! Ready to start honeypots."