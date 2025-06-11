# Create this file: ./honeypots/flask-fake-login/app.py

from flask import Flask, request, render_template_string
import logging
import os
from datetime import datetime

app = Flask(__name__)

# Ensure logs directory exists
os.makedirs('/app/logs', exist_ok=True)

# Set up logging to the mounted volume
logging.basicConfig(
    filename='/app/logs/login.log', 
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Corporate Portal</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; }
        .login-box { 
            width: 300px; margin: 100px auto; padding: 20px; 
            background: white; border: 1px solid #ddd; border-radius: 5px;
        }
        input { width: 100%; padding: 10px; margin: 5px 0; }
        input[type="submit"] { background: #007cba; color: white; border: none; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Corporate Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required/><br/>
            <input type="password" name="password" placeholder="Password" required/><br/>
            <input type="submit" value="Login"/>
        </form>
        {% if error %}
        <p style="color: red;">Invalid credentials. Please try again.</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        ip = request.remote_addr
        ua = request.headers.get('User-Agent', 'Unknown')
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Log the attempt
        log_msg = f"Login attempt from {ip} | UA: {ua} | Username: {username} | Password: {password}"
        logging.info(log_msg)
        
        # Always show error to make it look real
        error = True
        
        # Also print to console for debugging
        print(f"[HONEYPOT] {log_msg}")
    
    return render_template_string(HTML, error=error)

@app.route('/admin')
def admin():
    # Log admin access attempts
    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')
    logging.info(f"Admin page access from {ip} | UA: {ua}")
    return "Access Denied"

if __name__ == '__main__':
    print("Starting Flask honeypot on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False)