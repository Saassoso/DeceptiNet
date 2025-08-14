#!/usr/bin/env python3
from flask import Flask, request, render_template_string, jsonify, redirect
import json
import os
import random
from datetime import datetime, timedelta
import hashlib
import time

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

# Fixed login page with proper Tailwind CSS CDN
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureCorp - Employee Portal</title>
    <!-- FIXED: Proper Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Alternative CDN if above doesn't work -->
    <!-- <link href="https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/3.3.0/tailwind.min.css" rel="stylesheet"> -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <style>
        /* Custom animations and effects */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-30px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .fade-in { 
            animation: fadeIn 0.8s ease-out forwards; 
            opacity: 0;
        }
        
        .slide-in { 
            animation: slideIn 0.6s ease-out forwards; 
            opacity: 0;
        }
        
        .gradient-bg { 
            background: linear-gradient(135deg, #1e40af 0%, #7c3aed 50%, #db2777 100%);
            background-size: 400% 400%;
            animation: gradientShift 8s ease infinite;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .glass-effect { 
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        }
        
        .input-glow:focus {
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3), 0 0 20px rgba(59, 130, 246, 0.2);
        }
        
        .btn-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.3);
        }
        
        .floating {
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
    </style>
</head>
<body class="min-h-screen gradient-bg flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Background decorative elements -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
        <div class="absolute -top-1/2 -left-1/2 w-full h-full bg-white opacity-5 rounded-full blur-3xl"></div>
        <div class="absolute -bottom-1/2 -right-1/2 w-full h-full bg-purple-300 opacity-10 rounded-full blur-3xl"></div>
    </div>
    
    <div class="w-full max-w-md relative z-10">
        <!-- Company Header -->
        <div class="text-center mb-8 fade-in">
            <div class="bg-white bg-opacity-20 w-24 h-24 rounded-3xl mx-auto mb-6 flex items-center justify-center floating backdrop-blur-sm border border-white border-opacity-30">
                <i class="fas fa-shield-alt text-white text-4xl drop-shadow-lg"></i>
            </div>
            <h1 class="text-white text-4xl font-bold mb-2 drop-shadow-lg">SecureCorp</h1>
            <p class="text-white text-opacity-90 text-lg font-medium">Enterprise Security Portal</p>
        </div>

        <!-- Login Form -->
        <div class="glass-effect rounded-3xl shadow-2xl overflow-hidden slide-in" style="animation-delay: 0.2s;">
            <!-- Header -->
            <div class="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-8 text-center text-white relative">
                <div class="absolute inset-0 bg-black bg-opacity-10"></div>
                <div class="relative z-10">
                    <h2 class="text-3xl font-bold mb-2">Employee Login</h2>
                    <p class="text-blue-100 font-medium">Access your secure dashboard</p>
                </div>
            </div>

            <form method="POST" class="p-8 space-y-8">
                {% if error %}
                <div class="bg-red-50 border-l-4 border-red-500 p-6 rounded-xl shadow-sm slide-in" style="animation-delay: 0.4s;">
                    <div class="flex items-start">
                        <div class="flex-shrink-0">
                            <i class="fas fa-exclamation-triangle text-red-500 text-xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-red-800 font-bold text-lg">Authentication Failed</p>
                            <p class="text-red-600 mt-1">Invalid credentials. Access attempt has been logged for security review.</p>
                        </div>
                    </div>
                </div>
                {% endif %}

                <div class="space-y-6">
                    <!-- Username Field -->
                    <div class="slide-in" style="animation-delay: 0.3s;">
                        <label class="block text-gray-700 font-bold mb-3 text-lg" for="username">
                            <i class="fas fa-user mr-3 text-blue-600"></i>Username
                        </label>
                        <input 
                            type="text" 
                            id="username" 
                            name="username" 
                            class="w-full px-6 py-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-0 input-glow transition-all duration-300 text-lg font-medium bg-white shadow-sm"
                            placeholder="Enter your employee ID"
                            required
                        >
                    </div>

                    <!-- Password Field -->
                    <div class="slide-in" style="animation-delay: 0.4s;">
                        <label class="block text-gray-700 font-bold mb-3 text-lg" for="password">
                            <i class="fas fa-lock mr-3 text-purple-600"></i>Password
                        </label>
                        <div class="relative">
                            <input 
                                type="password" 
                                id="password" 
                                name="password" 
                                class="w-full px-6 py-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-0 input-glow transition-all duration-300 text-lg font-medium bg-white shadow-sm pr-12"
                                placeholder="Enter your password"
                                required
                            >
                            <button type="button" class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600" onclick="togglePassword()">
                                <i class="fas fa-eye" id="toggleIcon"></i>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Submit Button -->
                <button 
                    type="submit" 
                    class="w-full bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white font-bold py-4 px-6 rounded-xl btn-hover transition-all duration-300 shadow-lg text-lg slide-in"
                    style="animation-delay: 0.5s;"
                    id="loginBtn"
                >
                    <span class="flex items-center justify-center">
                        <i class="fas fa-sign-in-alt mr-3"></i>
                        <span id="btnText">Sign In Securely</span>
                        <i class="fas fa-spinner fa-spin ml-3 hidden" id="spinner"></i>
                    </span>
                </button>

                <!-- Links -->
                <div class="flex justify-between items-center pt-4 slide-in" style="animation-delay: 0.6s;">
                    <a href="/forgot-password" class="text-blue-600 hover:text-blue-800 transition-colors font-medium flex items-center">
                        <i class="fas fa-key mr-2"></i>Forgot Password?
                    </a>
                    <a href="/support" class="text-gray-600 hover:text-gray-800 transition-colors font-medium flex items-center">
                        <i class="fas fa-question-circle mr-2"></i>Need Help?
                    </a>
                </div>
            </form>

            <!-- Footer -->
            <div class="bg-gray-50 px-8 py-6 text-center border-t border-gray-100">
                <p class="text-gray-500 text-sm font-medium">
                    &copy; 2024 SecureCorp Inc. All rights reserved. 
                    <a href="/privacy" class="text-blue-600 hover:underline ml-2 font-semibold">Privacy Policy</a>
                </p>
            </div>
        </div>

        <!-- Security Notice -->
        <div class="mt-8 text-center fade-in" style="animation-delay: 0.7s;">
            <div class="bg-white bg-opacity-10 backdrop-blur-sm rounded-xl p-6 text-white border border-white border-opacity-20">
                <i class="fas fa-shield-alt mr-3 text-yellow-300"></i>
                <span class="font-medium">This is a secure connection. All login attempts are monitored and logged for security compliance.</span>
            </div>
        </div>
    </div>
    
    <script>
        // Form submission with enhanced UX
        document.querySelector('form').addEventListener('submit', function(e) {
            const btn = document.getElementById('loginBtn');
            const btnText = document.getElementById('btnText');
            const spinner = document.getElementById('spinner');
            
            // Show loading state
            btn.disabled = true;
            btn.classList.add('opacity-75', 'cursor-not-allowed');
            btnText.textContent = 'Authenticating...';
            spinner.classList.remove('hidden');
            
            // Prevent form from submitting immediately
            e.preventDefault();
            
            // Simulate realistic authentication delay
            setTimeout(() => {
                // Now submit the form
                e.target.submit();
            }, 2000);
        });

        // Enhanced input interactions
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('transform', 'scale-105');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('transform', 'scale-105');
            });
            
            // Add typing effect
            input.addEventListener('input', function() {
                if (this.value.length > 0) {
                    this.classList.add('bg-blue-50');
                } else {
                    this.classList.remove('bg-blue-50');
                }
            });
        });

        // Password visibility toggle
        function togglePassword() {
            const passwordInput = document.getElementById('password');
            const toggleIcon = document.getElementById('toggleIcon');
            
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleIcon.classList.remove('fa-eye');
                toggleIcon.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                toggleIcon.classList.remove('fa-eye-slash');
                toggleIcon.classList.add('fa-eye');
            }
        }

        // Add subtle parallax effect to background elements
        document.addEventListener('mousemove', function(e) {
            const mouseX = e.clientX / window.innerWidth;
            const mouseY = e.clientY / window.innerHeight;
            
            const bg1 = document.querySelector('.absolute.-top-1\\/2');
            const bg2 = document.querySelector('.absolute.-bottom-1\\/2');
            
            if (bg1) bg1.style.transform = `translate(${mouseX * 20}px, ${mouseY * 20}px)`;
            if (bg2) bg2.style.transform = `translate(${-mouseX * 15}px, ${-mouseY * 15}px)`;
        });
    </script>
</body>
</html>
'''

# Updated admin page with proper styling
ADMIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureCorp Admin Dashboard - Access Denied</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #1e3a8a 0%, #7c2d12 100%); }
        .pulse-red { 
            animation: pulse-red 2s infinite;
            box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
        }
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            70% { box-shadow: 0 0 0 20px rgba(239, 68, 68, 0); }
            100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
        }
        .glitch {
            animation: glitch 1s linear infinite;
        }
        @keyframes glitch {
            0%, 90% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
        }
    </style>
</head>
<body class="bg-gray-900 min-h-screen text-white">
    <!-- Header -->
    <nav class="bg-gray-800 shadow-2xl border-b border-red-600">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-6">
                <div class="flex items-center space-x-6">
                    <div class="bg-red-600 w-12 h-12 rounded-xl flex items-center justify-center pulse-red">
                        <i class="fas fa-shield-alt text-white text-xl"></i>
                    </div>
                    <div>
                        <h1 class="text-white text-2xl font-bold">SecureCorp Admin Portal</h1>
                        <p class="text-gray-300 text-sm font-medium">Security Management Dashboard</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4 text-red-400 glitch">
                    <i class="fas fa-exclamation-triangle text-2xl"></i>
                    <span class="font-bold text-lg">UNAUTHORIZED ACCESS DETECTED</span>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-6xl mx-auto py-16 px-4">
        <div class="bg-gray-800 rounded-3xl shadow-2xl overflow-hidden border border-red-500">
            <!-- Warning Header -->
            <div class="bg-gradient-to-r from-red-600 to-red-800 text-white p-8 text-center relative">
                <div class="absolute inset-0 bg-black bg-opacity-20"></div>
                <div class="relative z-10">
                    <div class="pulse-red w-24 h-24 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-6">
                        <i class="fas fa-ban text-4xl"></i>
                    </div>
                    <h2 class="text-4xl font-bold mb-4">ACCESS DENIED</h2>
                    <p class="text-red-100 text-xl font-semibold">HTTP 403 - Forbidden Resource</p>
                </div>
            </div>

            <!-- Content -->
            <div class="p-12">
                <div class="text-center mb-12">
                    <h3 class="text-3xl font-bold text-white mb-6">
                        Insufficient Privileges
                    </h3>
                    <p class="text-gray-300 text-xl leading-relaxed max-w-3xl mx-auto">
                        This administrative interface is restricted to authorized SecureCorp system administrators only. 
                        Your access attempt has been logged and security personnel have been notified.
                    </p>
                </div>

                <!-- Security Info Grid -->
                <div class="grid md:grid-cols-3 gap-8 mb-12">
                    <div class="bg-yellow-900 bg-opacity-50 border border-yellow-600 rounded-2xl p-6 backdrop-blur-sm">
                        <div class="flex items-start">
                            <i class="fas fa-exclamation-triangle text-yellow-400 text-2xl mr-4 mt-1"></i>
                            <div>
                                <h4 class="font-bold text-yellow-300 mb-3 text-lg">Security Alert</h4>
                                <p class="text-yellow-200 text-sm leading-relaxed">
                                    This incident has been automatically logged with your IP address, browser fingerprint, 
                                    and access timestamp for security analysis.
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-blue-900 bg-opacity-50 border border-blue-600 rounded-2xl p-6 backdrop-blur-sm">
                        <div class="flex items-start">
                            <i class="fas fa-user-shield text-blue-400 text-2xl mr-4 mt-1"></i>
                            <div>
                                <h4 class="font-bold text-blue-300 mb-3 text-lg">Need Access?</h4>
                                <p class="text-blue-200 text-sm leading-relaxed">
                                    Administrator credentials are required. Contact your IT security team 
                                    or system administrator for proper authorization.
                                </p>
                            </div>
                        </div>
                    </div>

                    <div class="bg-red-900 bg-opacity-50 border border-red-600 rounded-2xl p-6 backdrop-blur-sm">
                        <div class="flex items-start">
                            <i class="fas fa-eye text-red-400 text-2xl mr-4 mt-1"></i>
                            <div>
                                <h4 class="font-bold text-red-300 mb-3 text-lg">Monitoring Active</h4>
                                <p class="text-red-200 text-sm leading-relaxed">
                                    All access attempts to this system are actively monitored 
                                    and may trigger additional security measures.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- System Info -->
                <div class="bg-gray-700 rounded-2xl p-8 mb-8 border border-gray-600">
                    <h4 class="text-xl font-bold text-white mb-4 flex items-center">
                        <i class="fas fa-server mr-3 text-purple-400"></i>
                        Incident Details
                    </h4>
                    <div class="grid md:grid-cols-2 gap-6 text-sm font-mono">
                        <div class="space-y-2">
                            <p class="text-gray-300"><span class="text-purple-400">Timestamp:</span> <span id="timestamp"></span></p>
                            <p class="text-gray-300"><span class="text-purple-400">Request ID:</span> <span id="requestId"></span></p>
                        </div>
                        <div class="space-y-2">
                            <p class="text-gray-300"><span class="text-purple-400">Security Level:</span> <span class="text-red-400">CRITICAL</span></p>
                            <p class="text-gray-300"><span class="text-purple-400">Status:</span> <span class="text-red-400">ACCESS_DENIED</span></p>
                        </div>
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="text-center space-x-6">
                    <a href="/" class="inline-flex items-center px-8 py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
                        <i class="fas fa-home mr-3"></i>
                        Return to Login Portal
                    </a>
                    <a href="/support" class="inline-flex items-center px-8 py-4 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1">
                        <i class="fas fa-headset mr-3"></i>
                        Contact IT Support
                    </a>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Display current timestamp and generate request ID
        document.addEventListener('DOMContentLoaded', function() {
            const timestamp = new Date().toISOString();
            const requestId = 'REQ-' + Math.random().toString(36).substr(2, 9).toUpperCase();
            
            document.getElementById('timestamp').textContent = timestamp;
            document.getElementById('requestId').textContent = requestId;
        });

        // Add some dramatic effects
        setInterval(() => {
            const alerts = document.querySelectorAll('.pulse-red');
            alerts.forEach(alert => {
                alert.style.transform = `scale(${0.95 + Math.random() * 0.1})`;
            });
        }, 2000);
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
        time.sleep(random.uniform(2.0, 3.5))
       
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
def wordpress_probes():
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
    print("✅ Fixed Tailwind CSS integration")
    app.run(host='0.0.0.0', port=5000, debug=False)