from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# In-memory user database (replace with actual DB)
users = {
    "user1": generate_password_hash("password1"),
    "user2": generate_password_hash("password2")
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users[username] = generate_password_hash(password)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome, you are logged in!"

if __name__ == '__main__':
    app.run(debug=True)

# templates/index.html
<!DOCTYPE html>
<html>
  <body>
    <form action="{{ url_for('login') }}" method="post">
      <input type="text" name="username" placeholder="Username">
      <input type="password" name="password" placeholder="Password">
      <button type="submit">Login</button>
    </form>
    <a href="{{ url_for('register') }}">Register</a>
  </body>
</html>

# templates/login.html
<!DOCTYPE html>
<html>
  <body>
    <form action="" method="post">
      <input type="text" name="username" placeholder="Username">
      <input type="password" name="password" placeholder="Password">
      <button type="submit">Login</button>
    </form>
  </body>
</html>

# templates/register.html
<!DOCTYPE html>
<html>
  <body>
    <form action="" method="post">
      <input type="text" name="username" placeholder="Username">
      <input type="password" name="password" placeholder="Password">
      <button type="submit">Register</button>
    </form>
  </body>
</html>