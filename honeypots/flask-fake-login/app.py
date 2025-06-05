from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with open('login_attempts.log', 'a') as f:
            f.write(f"{datetime.now()} - USER: {request.form.get('username')} | PASS: {request.form.get('password')}\n")
        return "Invalid credentials"
    return '''
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

app.run(host='0.0.0.0', port=5000)
