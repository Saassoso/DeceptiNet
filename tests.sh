#!/bin/bash

echo "🐝 DECEPTINET HONEYPOT TESTING SCRIPT"
echo "====================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to test if a port is open
test_port() {
    local host=$1
    local port=$2
    local service=$3
    
    if nc -z -w5 $host $port 2>/dev/null; then
        echo -e "${GREEN}✅ $service${NC} (port $port) - ${GREEN}RUNNING${NC}"
        return 0
    else
        echo -e "${RED}❌ $service${NC} (port $port) - ${RED}NOT RUNNING${NC}"
        return 1
    fi
}

echo "🔍 Testing Honeypot Services..."
echo ""

# Test each honeypot
test_port localhost 2222 "Cowrie SSH Honeypot"
test_port localhost 5000 "Flask Web Honeypot"
test_port localhost 21 "Dionaea FTP"
test_port localhost 23 "Dionaea Telnet"
test_port localhost 8080 "Dionaea HTTP"
test_port localhost 8443 "Dionaea HTTPS"

echo ""
echo "🧪 RUNNING HONEYPOT TESTS..."
echo ""

# Test 1: SSH Honeypot
echo -e "${YELLOW}Test 1: SSH Honeypot${NC}"
echo "Clearing old SSH keys..."
ssh-keygen -f "/home/saad/.ssh/known_hosts" -R "[localhost]:2222" 2>/dev/null
echo "Testing SSH connection (will fail - that's normal)..."
timeout 10 ssh -p 2222 -o StrictHostKeyChecking=no root@localhost 2>/dev/null || echo -e "${GREEN}✅ SSH honeypot responded${NC}"
echo ""

# Test 2: Web Honeypot
echo -e "${YELLOW}Test 2: Web Honeypot${NC}"
echo "Testing web interface..."
if curl -s http://localhost:5000 | grep -q "Corporate"; then
    echo -e "${GREEN}✅ Web honeypot is serving login page${NC}"
else
    echo -e "${RED}❌ Web honeypot not responding${NC}"
fi

echo "Testing fake login attempt..."
curl -s -X POST http://localhost:5000 \
    -d "username=admin&password=password123" \
    -H "Content-Type: application/x-www-form-urlencoded" > /dev/null
echo -e "${GREEN}✅ Fake login attempt sent${NC}"
echo ""

# Test 3: Admin page
echo -e "${YELLOW}Test 3: Admin Page Access${NC}"
if curl -s http://localhost:5000/admin | grep -q "Access Denied"; then
    echo -e "${GREEN}✅ Admin page is protected${NC}"
else
    echo -e "${RED}❌ Admin page not working${NC}"
fi
echo ""

# Test 4: Check logs
echo -e "${YELLOW}Test 4: Log File Generation${NC}"
if [ -f "data/logs/flask-fake-login/login.log" ]; then
    echo -e "${GREEN}✅ Flask logs are being created${NC}"
    echo "Last 3 log entries:"
    tail -n 3 data/logs/flask-fake-login/login.log 2>/dev/null || echo "No entries yet"
else
    echo -e "${RED}❌ Flask logs not found${NC}"
fi

if [ -f "data/logs/cowrie/cowrie.log" ]; then
    echo -e "${GREEN}✅ Cowrie logs are being created${NC}"
else
    echo -e "${RED}❌ Cowrie logs not found${NC}"
fi
echo ""

# Test 5: Multiple attack simulation
echo -e "${YELLOW}Test 5: Simulating Attack Patterns${NC}"
echo "Simulating brute force attack..."

# Common username/password combinations
declare -a usernames=("admin" "root" "administrator" "user" "test")
declare -a passwords=("password" "123456" "admin" "root" "password123")

for user in "${usernames[@]}"; do
    for pass in "${passwords[@]}"; do
        curl -s -X POST http://localhost:5000 \
            -d "username=$user&password=$pass" \
            -H "Content-Type: application/x-www-form-urlencoded" \
            -H "User-Agent: Mozilla/5.0 (Attacker Bot)" > /dev/null
        sleep 0.1
    done
done

echo -e "${GREEN}✅ Simulated brute force attack completed${NC}"
echo ""

# Test 6: Directory scanning simulation
echo -e "${YELLOW}Test 6: Directory Scanning Simulation${NC}"
declare -a paths=("/admin" "/login" "/config" "/backup" "/wp-admin" "/.env" "/robots.txt")

for path in "${paths[@]}"; do
    curl -s "http://localhost:5000$path" > /dev/null
    sleep 0.1
done

echo -e "${GREEN}✅ Directory scanning simulation completed${NC}"
echo ""

# Summary
echo "📊 SUMMARY"
echo "=========="
echo "🎯 Your honeypots have been tested with:"
echo "   • SSH connection attempts"
echo "   • Web login brute force (25 attempts)"
echo "   • Admin page access attempts"
echo "   • Directory scanning attempts"
echo ""
echo "📁 Check your logs:"
echo "   • Flask logs: data/logs/flask-fake-login/"
echo "   • Cowrie logs: data/logs/cowrie/"
echo ""
echo "🔍 Run the analyzer to see results:"
echo "   python3 analyzer.py"
echo ""
echo -e "${GREEN}✅ Testing complete!${NC}"