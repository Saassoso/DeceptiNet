#!/usr/bin/env python3
from flask import Flask, request, render_template_string, jsonify, redirect
import json
import os
import random
from datetime import datetime, timedelta
import hashlib

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
        'referer': request.headers.get('Referer', ''),
        'data': data
    }
   
    with open('/app/logs/attacks.json', 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
   
    print(f"[ATTACK] {event_type} from {request.remote_addr}")

# Modern corporate login page with CDN Tailwind CSS
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureCorp - Employee Portal</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in { animation: fadeIn 0.8s ease-out; }
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .glass-effect { 
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
    </style>
</head>
<body class="min-h-screen gradient-bg flex items-center justify-center p-4">
    <div class="w-full max-w-md">
        <!-- Company Header -->
        <div class="text-center mb-8 fade-in">
            <div class="bg-white bg-opacity-20 w-20 h-20 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                <i class="fas fa-shield-alt text-white text-3xl"></i>
            </div>
            <h1 class="text-white text-3xl font-bold mb-2">SecureCorp</h1>
            <p class="text-white text-opacity-90">Enterprise Security Portal</p>
        </div>

        <!-- Login Form -->
        <div class="glass-effect rounded-2xl shadow-2xl overflow-hidden fade-in">
            <div class="bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-center text-white">
                <h2 class="text-2xl font-semibold mb-2">Employee Login</h2>
                <p class="text-blue-100">Access your secure dashboard</p>
            </div>

            <form method="POST" class="p-8 space-y-6">
                {% if error %}
                <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                    <div class="flex items-center">
                        <i class="fas fa-exclamation-triangle text-red-500 mr-3"></i>
                        <div>
                            <p class="text-red-800 font-semibold">Authentication Failed</p>
                            <p class="text-red-600 text-sm">Invalid credentials. Access attempt logged.</p>
                        </div>
                    </div>
                </div>
                {% endif %}

                <div class="space-y-4">
                    <div>
                        <label class="block text-gray-700 font-semibold mb-2" for="username">
                            <i class="fas fa-user mr-2"></i>Username
                        </label>
                        <input 
                            type="text" 
                            id="username" 
                            name="username" 
                            class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
                            placeholder="Enter your username"
                            required
                        >
                    </div>

                    <div>
                        <label class="block text-gray-700 font-semibold mb-2" for="password">
                            <i class="fas fa-lock mr-2"></i>Password
                        </label>
                        <input 
                            type="password" 
                            id="password" 
                            name="password" 
                            class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all duration-200"
                            placeholder="Enter your password"
                            required
                        >
                    </div>
                </div>

                <button 
                    type="submit" 
                    class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 px-4 rounded-lg hover:from-blue-700 hover:to-purple-700 transform hover:-translate-y-0.5 transition-all duration-200 shadow-lg hover:shadow-xl"
                    id="loginBtn"
                >
                    <span class="flex items-center justify-center">
                        <i class="fas fa-sign-in-alt mr-2"></i>
                        <span id="btnText">Sign In</span>
                        <i class="fas fa-spinner fa-spin ml-2 hidden" id="spinner"></i>
                    </span>
                </button>

                <div class="flex justify-between items-center text-sm">
                    <a href="/forgot-password" class="text-blue-600 hover:text-blue-800 transition-colors">
                        <i class="fas fa-key mr-1"></i>Forgot Password?
                    </a>
                    <a href="/support" class="text-gray-600 hover:text-gray-800 transition-colors">
                        <i class="fas fa-question-circle mr-1"></i>Need Help?
                    </a>
                </div>
            </form>

            <!-- Footer -->
            <div class="bg-gray-50 px-8 py-4 text-center border-t">
                <p class="text-gray-500 text-xs">
                    &copy; 2024 SecureCorp Inc. All rights reserved. 
                    <a href="/privacy" class="text-blue-600 hover:underline ml-1">Privacy Policy</a>
                </p>
            </div>
        </div>

        <!-- Security Notice -->
        <div class="mt-6 text-center fade-in">
            <div class="bg-white bg-opacity-10 rounded-lg p-4 text-white text-sm">
                <i class="fas fa-info-circle mr-2"></i>
                This is a secure connection. Your login attempts are monitored for security purposes.
            </div>
        </div>
    </div>
    
    <script>
        // Form submission handling
        document.querySelector('form').addEventListener('submit', function(e) {
            const btn = document.getElementById('loginBtn');
            const btnText = document.getElementById('btnText');
            const spinner = document.getElementById('spinner');
            
            // Show loading state
            btn.disabled = true;
            btnText.textContent = 'Authenticating...';
            spinner.classList.remove('hidden');
            btn.classList.add('opacity-75');
            
            // Simulate processing time
            setTimeout(() => {
                // Form will submit normally
            }, 1500);
        });

        // Enhanced input interactions
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('transform', 'scale-105');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('transform', 'scale-105');
            });
        });

        // Add floating labels effect
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.classList.add('has-content');
                } else {
                    this.classList.remove('has-content');
                }
            });
        });
    </script>
</body>
</html>
'''

# Modern admin dashboard honeypot
ADMIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureCorp Admin Dashboard - Access Denied</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #1e3a8a 0%, #7c2d12 100%); }
        .pulse-red { animation: pulse-red 2s infinite; }
        @keyframes pulse-red {
            0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            50% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <!-- Header -->
    <nav class="bg-gray-800 shadow-lg">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center space-x-4">
                    <div class="bg-red-600 w-10 h-10 rounded-lg flex items-center justify-center">
                        <i class="fas fa-shield-alt text-white"></i>
                    </div>
                    <div>
                        <h1 class="text-white text-xl font-bold">SecureCorp Admin</h1>
                        <p class="text-gray-300 text-sm">Security Management Portal</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4 text-red-400">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span class="font-semibold">UNAUTHORIZED ACCESS</span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-4xl mx-auto py-12 px-4">
        <div class="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <!-- Warning Header -->
            <div class="bg-red-600 text-white p-6 text-center">
                <div class="pulse-red w-20 h-20 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                    <i class="fas fa-ban text-3xl"></i>
                </div>
                <h2 class="text-3xl font-bold mb-2">Access Denied</h2>
                <p class="text-red-100">HTTP 403 - Forbidden</p>
            </div>

            <!-- Content -->
            <div class="p-8">
                <div class="text-center mb-8">
                    <h3 class="text-2xl font-semibold text-gray-800 mb-4">
                        You do not have permission to access this resource
                    </h3>
                    <p class="text-gray-600 text-lg leading-relaxed">
                        This area is restricted to authorized SecureCorp administrators only. 
                        All access attempts are monitored and logged for security purposes.
                    </p>
                </div>

                <!-- Security Info -->
                <div class="grid md:grid-cols-2 gap-6 mb-8">
                    <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                        <div class="flex items-start">
                            <i class="fas fa-info-circle text-yellow-600 text-xl mr-3 mt-1"></i>
                            <div>
                                <h4 class="font-semibold text-yellow-800 mb-2">Security Notice</h4>
                                <p class="text-yellow-700 text-sm">
                                    This incident has been logged with your IP address, timestamp, and browser information.
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                        <div class="flex items-start">
                            <i class="fas fa-user-shield text-blue-600 text-xl mr-3 mt-1"></i>
                            <div>
                                <h4 class="font-semibold text-blue-800 mb-2">Need Access?</h4>
                                <p class="text-blue-700 text-sm">
                                    Contact your system administrator to request proper credentials.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="text-center space-x-4">
                    <a href="/" class="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors">
                        <i class="fas fa-home mr-2"></i>
                        Return to Login
                    </a>
                    <a href="/support" class="inline-flex items-center px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition-colors">
                        <i class="fas fa-question-circle mr-2"></i>
                        Contact Support
                    </a>
                </div>
            </div>

            <!-- Footer -->
            <div class="bg-gray-50 px-8 py-4 border-t text-center">
                <p class="text-gray-500 text-sm">
                    <i class="fas fa-clock mr-1"></i>
                    Incident logged at: <span class="font-mono">{{ timestamp }}</span>
                </p>
            </div>
        </div>
    </div>

    <script>
        // Display current timestamp
        document.addEventListener('DOMContentLoaded', function() {
            const timestamp = new Date().toISOString();
            const timestampElement = document.querySelector('[class*="font-mono"]');
            if (timestampElement) {
                timestampElement.textContent = timestamp;
            }
        });
    </script>
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
            'password': password,
            'form_data': dict(request.form)
        })
       
        # Add realistic delay for failed login
        import time
        time.sleep(random.uniform(1.5, 3.0))
       
        return render_template_string(LOGIN_HTML, error=True)
   
    log_attack('PAGE_VISIT', {'path': '/', 'method': 'GET'})
    return render_template_string(LOGIN_HTML)

@app.route('/admin')
def admin():
    log_attack('ADMIN_ACCESS', {'path': '/admin'})
    return render_template_string(ADMIN_HTML), 403

@app.route('/dashboard')
def dashboard():
    log_attack('DASHBOARD_ACCESS', {'path': '/dashboard'})
    return redirect('/')

@app.route('/api/<path:endpoint>')
def api_endpoints(endpoint):
    log_attack('API_PROBE', {'endpoint': endpoint, 'method': request.method})
    return jsonify({'error': 'Authentication required', 'code': 401}), 401

@app.route('/robots.txt')
def robots():
    log_attack('ROBOTS_ACCESS', {'path': '/robots.txt'})
    robots_content = """User-agent: *
Disallow: /admin/
Disallow: /dashboard/
Disallow: /api/
Disallow: /backup/
Disallow: /config/
Disallow: /logs/
Disallow: /private/
Disallow: /.env
Disallow: /db/

# Employee access only
Disallow: /hr/
Disallow: /payroll/
Disallow: /internal/"""
    return robots_content, 200, {'Content-Type': 'text/plain'}

@app.route('/sitemap.xml')
def sitemap():
    log_attack('SITEMAP_ACCESS', {'path': '/sitemap.xml'})
    sitemap_content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://securecorp.local/</loc><changefreq>daily</changefreq></url>
    <url><loc>https://securecorp.local/about</loc><changefreq>weekly</changefreq></url>
    <url><loc>https://securecorp.local/contact</loc><changefreq>weekly</changefreq></url>
    <url><loc>https://securecorp.local/admin</loc><changefreq>never</changefreq></url>
</urlset>'''
    return sitemap_content, 200, {'Content-Type': 'application/xml'}

@app.route('/forgot-password')
def forgot_password():
    log_attack('FORGOT_PASSWORD', {'path': '/forgot-password'})
    return "Password reset functionality is temporarily disabled for security reasons.", 503

@app.route('/support')
def support():
    log_attack('SUPPORT_ACCESS', {'path': '/support'})
    return "Support portal is currently under maintenance. Please contact your system administrator.", 503

@app.route('/privacy')
def privacy():
    log_attack('PRIVACY_ACCESS', {'path': '/privacy'})
    return "Privacy policy page - Under construction", 200

# Common attack vectors
@app.route('/.env')
def env_file():
    log_attack('ENV_FILE_ACCESS', {'path': '/.env'})
    return "Access Denied", 403

@app.route('/wp-admin')
@app.route('/wp-login.php')
@app.route('/wordpress')
def wordpress_probes(path=None):
    log_attack('WORDPRESS_PROBE', {'path': request.path})
    return "Not Found", 404

@app.route('/phpmyadmin')
@app.route('/pma')
@app.route('/mysql')
def db_probes():
    log_attack('DATABASE_PROBE', {'path': request.path})
    return "Not Found", 404

@app.route('/backup')
@app.route('/backup.zip')
@app.route('/backup.sql')
@app.route('/database.sql')
def backup_probes():
    log_attack('BACKUP_PROBE', {'path': request.path})
    return "Access Denied", 403

@app.route('/config')
@app.route('/config.php')
@app.route('/configuration')
def config_probes():
    log_attack('CONFIG_PROBE', {'path': request.path})
    return "Access Denied", 403

# Catch-all for other probes
@app.route('/<path:path>')
def catch_all(path):
    log_attack('PATH_PROBE', {'path': path, 'full_path': request.full_path})
    return "Not Found", 404

@app.errorhandler(404)
def not_found(error):
    log_attack('404_ERROR', {'path': request.path, 'error': str(error)})
    return "Page not found", 404

@app.errorhandler(500)
def server_error(error):
    log_attack('SERVER_ERROR', {'path': request.path, 'error': str(error)})
    return "Internal server error", 500

if __name__ == '__main__':
    print("🍯 Starting Advanced Web Honeypot on port 5000...")
    print("📊 Logs will be saved to /app/logs/attacks.json")
    print("🎭 Masquerading as SecureCorp Employee Portal")
    app.run(host='0.0.0.0', port=5000, debug=False)