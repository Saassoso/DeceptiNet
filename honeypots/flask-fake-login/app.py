from flask import Flask, request, render_template_string, jsonify
import logging
import os
import json
from datetime import datetime
import socket

app = Flask(__name__)

# Ensure logs directory exists
log_dir = '/app/logs'
os.makedirs(log_dir, exist_ok=True)

# Set up multiple logging formats
log_file = os.path.join(log_dir, 'login.log')
json_log_file = os.path.join(log_dir, 'login.json')

# Text logger
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# JSON logger for structured data
json_logger = logging.getLogger('json_logger')
json_handler = logging.FileHandler(json_log_file)
json_handler.setLevel(logging.INFO)
json_logger.addHandler(json_handler)
json_logger.setLevel(logging.INFO)

def log_event(event_type, data):
    """Log events in both text and JSON format"""
    timestamp = datetime.now().isoformat()
    
    # Text log
    logging.info(f"{event_type}: {data}")
    
    # JSON log
    json_entry = {
        'timestamp': timestamp,
        'event_type': event_type,
        'data': data
    }
    json_logger.info(json.dumps(json_entry))
    
    # Console output for debugging
    print(f"[HONEYPOT-{event_type}] {data}")

HTML_LOGIN = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Corporate Portal - Login</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
            font-size: 28px;
            font-weight: bold;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: 500;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .login-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .login-btn:hover {
            transform: translateY(-2px);
        }
        .error-msg {
            background: #fee;
            color: #c33;
            padding: 10px;
            border-radius: 5px;
            margin-top: 15px;
            border-left: 4px solid #c33;
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
            margin: 0 10px;
        }
        .links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">🏢 CorporateNet</div>
        <form method="POST" id="loginForm">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="login-btn">Sign In</button>
        </form>
        
        {% if error %}
        <div class="error-msg">
            <strong>Login Failed:</strong> Invalid username or password. Please try again.
        </div>
        {% endif %}
        
        <div class="links">
            <a href="/forgot-password">Forgot Password?</a>
            <a href="/admin">Admin Panel</a>
        </div>
    </div>

    <script>
        // Add some client-side behavior tracking
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            // Track form submission timing
            const formData = new FormData(this);
            formData.append('client_time', new Date().toISOString());
            formData.append('screen_resolution', screen.width + 'x' + screen.height);
            formData.append('timezone', Intl.DateTimeFormat().resolvedOptions().timeZone);
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = False
    
    if request.method == 'POST':
        # Collect comprehensive data about the attempt
        attempt_data = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'username': request.form.get('username', ''),
            'password': request.form.get('password', ''),
            'referer': request.headers.get('Referer', 'Direct'),
            'accept_language': request.headers.get('Accept-Language', 'Unknown'),
            'x_forwarded_for': request.headers.get('X-Forwarded-For', None),
            'client_time': request.form.get('client_time', 'Unknown'),
            'screen_resolution': request.form.get('screen_resolution', 'Unknown'),
            'timezone': request.form.get('timezone', 'Unknown'),
            'method': request.method,
            'content_type': request.content_type
        }
        
        log_event('LOGIN_ATTEMPT', attempt_data)
        
        # Always show error to maintain deception
        error = True
    
    else:  # GET request
        visit_data = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'referer': request.headers.get('Referer', 'Direct'),
            'accept_language': request.headers.get('Accept-Language', 'Unknown')
        }
        log_event('PAGE_VISIT', visit_data)
    
    return render_template_string(HTML_LOGIN, error=error)

@app.route('/admin')
def admin():
    admin_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'referer': request.headers.get('Referer', 'Direct')
    }
    log_event('ADMIN_ACCESS_ATTEMPT', admin_data)
    
    return '''
    <html>
    <head><title>Access Denied</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1 style="color: red;"> Access Denied</h1>
        <p>You don't have permission to access this resource.</p>
        <p><a href="/">Return to Login</a></p>
    </body>
    </html>
    ''', 403

@app.route('/forgot-password')
def forgot_password():
    forgot_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    log_event('FORGOT_PASSWORD_ACCESS', forgot_data)
    
    return '''
    <html>
    <head><title>Password Reset</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1> Password Reset</h1>
        <p>Password reset functionality is currently disabled.</p>
        <p>Please contact your system administrator.</p>
        <p><a href="/">Return to Login</a></p>
    </body>
    </html>
    '''

@app.route('/robots.txt')
def robots():
    robots_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    log_event('ROBOTS_TXT_ACCESS', robots_data)
    
    return '''User-agent: *
Disallow: /admin
Disallow: /backup
Disallow: /config
Disallow: /.env
''', 200, {'Content-Type': 'text/plain'}

@app.route('/api/status')
def api_status():
    api_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')
    }
    log_event('API_ACCESS', api_data)
    
    return jsonify({
        'status': 'online',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    error_data = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'requested_path': request.path,
        'method': request.method
    }
    log_event('404_ERROR', error_data)
    
    return '''
    <html>
    <head><title>404 - Page Not Found</title></head>
    <body style="font-family: Arial; text-align: center; margin-top: 100px;">
        <h1>404 - Page Not Found</h1>
        <p>The requested page could not be found.</p>
        <p><a href="/">Return to Login</a></p>
    </body>
    </html>
    ''', 404

if __name__ == '__main__':
    print("🐝 Starting Flask Honeypot Server...")
    print(f"📁 Logs directory: {log_dir}")
    print(f"📝 Log files: {log_file}, {json_log_file}")
    print("🌐 Server running on http://0.0.0.0:5000")
    print("🎯 Ready to catch attackers!")
    
    # Test log write on startup
    startup_data = {
        'event': 'honeypot_startup',
        'hostname': socket.gethostname(),
        'log_dir': log_dir
    }
    log_event('SYSTEM_STARTUP', startup_data)
    
    app.run(host='0.0.0.0', port=5000, debug=False)