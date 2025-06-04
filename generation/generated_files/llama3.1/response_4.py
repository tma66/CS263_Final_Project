from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post = Post(title=request.form['title'], content=request.form['content'], user_id=User.query.filter_by(username=current_user.username).first().id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('new_post.html')

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    if request.method == 'POST':
        keyword = request.form['keyword']
        posts = Post.query.filter(Post.title.like('%' + keyword + '%')).all()
        return render_template('index.html', posts=posts)
    return render_template('filter.html')

@app.route('/user/<username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('user_posts.html', username=username, posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

# templates/index.html
{% for post in posts %}
  <h1>{{ post.title }}</h1>
  {{ post.content }}
{% endfor %}

# templates/new_post.html
<form method="POST">
  <input type="text" name="title" placeholder="Post title">
  <textarea name="content"></textarea>
  <button type="submit">Submit</button>
</form>

# templates/filter.html
<form method="POST">
  <input type="text" name="keyword" placeholder="Keyword to filter posts by">
  <button type="submit">Filter</button>
</form>

# templates/user_posts.html
<h1>{{ username }}</h1>
{% for post in posts %}
  <h2>{{ post.title }}</h2>
  {{ post.content }}
{% endfor %}

# models.py (part of flask_sqlalchemy)
from flask import Flask, g

def init_db():
    db.create_all()

@app.before_request
def before_request():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            g.current_user = user

@app.teardown_appcontext
def teardown_appcontext(exc):
    if hasattr(g, 'current_user'):
        del g.current_user

# views.py (part of Flask)
from flask import render_template, request, redirect, url_for, flash
from .models import User, Post

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user_id'] = user.id
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')