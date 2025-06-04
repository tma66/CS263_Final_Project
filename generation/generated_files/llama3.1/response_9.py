from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/filter')
def filter_users():
    query_params = request.args
    email_filter = query_params.get('email')
    role_filter = query_params.get('role')
    date_from = query_params.get('date_from')
    date_to = query_params.get('date_to')

    if email_filter:
        users = User.query.filter(User.email.like('%' + email_filter + '%')).all()
    elif role_filter:
        users = User.query.filter_by(role=role_filter).all()
    elif date_from and date_to:
        users = User.query.filter((User.registration_date >= datetime.strptime(date_from, '%Y-%m-%d')) & 
                                  (User.registration_date <= datetime.strptime(date_to, '%Y-%m-%d'))).all()
    else:
        users = User.query.all()

    return render_template('index.html', users=users)

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)