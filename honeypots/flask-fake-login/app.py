from flask import Flask, request, render_template_string
import logging

app = Flask(__name__)
logging.basicConfig(filename='login.log', level=logging.INFO)

HTML = '''
<form method="POST">
  <input type="text" name="username" placeholder="Username"/><br/>
  <input type="password" name="password" placeholder="Password"/><br/>
  <input type="submit" value="Login"/>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ip = request.remote_addr
        ua = request.headers.get('User-Agent')
        username = request.form['username']
        password = request.form['password']
        logging.info(f"Login attempt from {ip}, UA: {ua}, Username: {username}, Password: {password}")
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
