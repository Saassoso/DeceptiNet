#!/bin/bash
echo "🔍 Testing Dionaea inetutils-ftp Service..."

# Test 1: Anonymous inetutils-ftp login
inetutils-ftp -n localhost 21 << 'EOF'
user anonymous anonymous
pwd
ls
quit
EOF

# Test 2: Brute force inetutils-ftp
declare -a users=("admin" "root" "inetutils-ftp" "user")
declare -a passes=("password" "123456" "admin" "inetutils-ftp")

for user in "${users[@]}"; do
    for pass in "${passes[@]}"; do
        echo "Testing inetutils-ftp: $user:$pass"
        inetutils-ftp -n localhost 21 << EOF
user $user $pass
quit
EOF
        sleep 1
    done
done