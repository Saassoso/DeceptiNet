#!/usr/bin/env python3

from flask import Flask, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# Create logs directory
os.makedirs('/app/logs', exist_ok=True)

def log_attack(event_type, data):
    """Log attack attempts to JSON file"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'event': event_type,
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', ''),
        'data': data
    }
    
    with open('/app/logs/attacks.json', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
    
    print(f"[ATTACK] {event_type} from {request.remote_addr}")

# Fake login page
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <style>
        body { font-family: Arial; max-width: 400px; margin: 100px auto; }
        .login-box { border: 1px solid #ccc; padding: 20px; }
        input { width: 100%; padding: 10px; margin: 5px 0; }
        button { width: 100%; padding: 10px; background: #007cba; color: white; border: none; }
        .error { color: red; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>System Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
        <div class="error">Invalid credentials!</div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        log_attack('LOGIN_ATTEMPT', {
            'username': username,
            'password': password
        })
        
        return render_template_string(LOGIN_HTML, error=True)
    
    log_attack('PAGE_VISIT', {'path': '/'})
    return render_template_string(LOGIN_HTML)

@app.route('/admin')
def admin():
    log_attack('ADMIN_ACCESS', {'path': '/admin'})
    return "Access Denied", 403

@app.route('/robots.txt')
def robots():
    log_attack('ROBOTS_ACCESS', {'path': '/robots.txt'})
    return "User-agent: *\nDisallow: /admin\nDisallow: /backup"

@app.route('/<path:path>')
def catch_all(path):
    log_attack('PATH_PROBE', {'path': path})
    return "Not Found", 404

if __name__ == '__main__':
    print("Starting Web Honeypot on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)