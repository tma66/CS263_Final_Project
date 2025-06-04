import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Connect to SQLite database. It will be created if it doesn't exist.
conn = sqlite3.connect('blog.db')
cursor = conn.cursor()

# Create table for users
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Create table for posts
cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES users(id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Connect to the database and create a new user entry
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, password))
        conn.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connect to the database and retrieve the user's entry
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('admin_panel'))

    return render_template('login.html')

# Route for the admin panel
@app.route('/admin', methods=['GET'])
def admin_panel():
    return render_template('admin.html')

# Route to search users by name or email
@app.route('/search/users', methods=['POST'])
def search_users():
    query = request.form['query']
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name LIKE ? OR email LIKE ?", ('%' + query + '%', '%' + query + '%'))
    users = cursor.fetchall()

    return render_template('users.html', users=users)

# Route to search posts by title or content
@app.route('/search/posts', methods=['POST'])
def search_posts():
    query = request.form['query']
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?", ('%' + query + '%', '%' + query + '%'))
    posts = cursor.fetchall()

    return render_template('posts.html', posts=posts)

# Route to delete a user
@app.route('/delete/user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

    return redirect(url_for('admin_panel'))

# Route to delete a post
@app.route('/delete/post/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=?", (post_id,))
    conn.commit()

    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

<!-- register.html -->

<form method="post">
    <label for="name">Name:</label>
    <input type="text" id="name" name="name"><br><br>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email"><br><br>
    <label for="password">Password:</label>
    <input type="password" id="password" name="password"><br><br>
    <input type="submit" value="Register">
</form>

<!-- login.html -->

<form method="post">
    <label for="email">Email:</label>
    <input type="email" id="email" name="email"><br><br>
    <label for="password">Password:</label>
    <input type="password" id="password" name="password"><br><br>
    <input type="submit" value="Login">
</form>

<!-- admin.html -->

<h1>Admin Panel</h1>

<form method="post" action="/search/users">
    <label for="query">Search Users:</label>
    <input type="text" id="query" name="query"><br><br>
    <input type="submit" value="Search">
</form>

<form method="post" action="/search/posts">
    <label for="query">Search Posts:</label>
    <input type="text" id="query" name="query"><br><br>
    <input type="submit" value="Search">
</form>

<!-- users.html -->

<h1>Users</h1>

<ul>
    {% for user in users %}
        <li>{{ user[1] }} ({{ user[2] }})</li>
    {% endfor %}
</ul>

<!-- posts.html -->

<h1>Posts</h1>

<ul>
    {% for post in posts %}
        <li>{{ post[1] }} by {{ post[3] }}</li>
    {% endfor %}
</ul>