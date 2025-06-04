from flask import Flask, render_template, request, redirect, url_for
import markdown
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/admin')
def admin():
    posts = Post.query.all()
    return render_template('admin.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    html_content = markdown.markdown(post.content)
    return render_template('post.html', post=post, content=html_content)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('create.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect(url_for('admin'))
    html_content = markdown.markdown(post.content)
    return render_template('edit.html', post=post, content=html_content)

@app.route('/preview', methods=['POST'])
def preview():
    content = request.form['content']
    html_content = markdown.markdown(content)
    return html_content

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)