#!/bin/bash

echo "🐝 DECEPTINET COMPREHENSIVE TESTING"
echo "==================================="

# Function to test SSH honeypot
test_ssh() {
    echo "🔍 Testing SSH Honeypot (Cowrie)..."
    
    # Test multiple login attempts
    declare -a users=("root" "admin" "user" "test")
    declare -a passes=("password" "123456" "root" "admin")
    
    for user in "${users[@]}"; do
        for pass in "${passes[@]}"; do
            echo "Trying $user:$pass"
            sshpass -p "$pass" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 -p 2222 "$user@localhost" "echo test" 2>/dev/null &
            sleep 1
        done
    done
    
    # Wait for connections to complete
    wait
    echo "✅ SSH brute force test completed"
}

test_ftp() {
    echo "🔍 Testing FTP Honeypot (Dionaea)..."
    
    # Test FTP connection
    timeout 10 ftp -n localhost 21 << 'EOF' 2>/dev/null
user anonymous anonymous
quit
EOF
    
    echo "✅ FTP test completed"
}

# Install required tools if not present
if ! command -v sshpass &> /dev/null; then
    echo "Installing sshpass..."
    sudo apt-get update && sudo apt-get install -y sshpass ftp
fi

# Run tests
test_ssh
test_ftp

echo ""
echo "📊 Check logs now:"
echo "docker-compose logs cowrie"
echo "docker-compose logs dionaea"
echo "ls -la data/logs/*/."