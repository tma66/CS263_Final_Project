import flask
from flask import render_template, request, redirect, url_for
import markdown
from datetime import datetime

app = flask.Flask(__name__)

# Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    return render_template('admin.html')

# Post History
@app.route('/history')
def post_history():
    posts = [
        {'title': 'Post 1', 'content': 'Markdown content here'},
        {'title': 'Post 2', 'content': 'More Markdown content here'}
    ]
    return render_template('history.html', posts=posts)

# Create Post
@app.route('/post/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = markdown.markdown(request.form['content'], extensions=['fenced_code'])
        post = {'title': title, 'content': content}
        # Store post in database (e.g., SQLite)
        return redirect(url_for('post_history'))
    else:
        return render_template('new_post.html')

# View Post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    # Retrieve post from database by ID
    post = {'title': 'Post 1', 'content': 'Markdown content here'}
    return render_template('view_post.html', post=post)

# Live Markdown Preview
@app.route('/preview', methods=['POST'])
def live_preview():
    content = request.form['content']
    preview = markdown.markdown(content, extensions=['fenced_code'])
    return {'preview': preview}

if __name__ == '__main__':
    app.run(debug=True)

# Templates

# admin.html
{% extends 'base.html' %}

{% block content %}
  <h1>Admin Dashboard</h1>
  <p>This is the admin dashboard.</p>
{% endblock %}

# history.html
{% extends 'base.html' %}

{% block content %}
  <h1>Post History</h1>
  {% for post in posts %}
    <article>
      <h2>{{ post.title }}</h2>
      {{ post.content | safe }}
    </article>
  {% endfor %}
{% endblock %}

# new_post.html
{% extends 'base.html' %}

{% block content %}
  <h1>Create New Post</h1>
  <form action="{{ url_for('create_post') }}" method="post">
    <input type="text" name="title" placeholder="Title">
    <textarea name="content"></textarea>
    <button type="submit">Create Post</button>
  </form>
{% endblock %}

# view_post.html
{% extends 'base.html' %}

{% block content %}
  <h1>{{ post.title }}</h1>
  {{ post.content | safe }}
{% endblock %}

# base.html
<!DOCTYPE html>
<html>
<head>
  <title>Blog</title>
</head>
<body>
  {% block content %}{% endblock %}
</body>
</html>