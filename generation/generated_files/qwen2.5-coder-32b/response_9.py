from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)

@app.route('/admin/users', methods=['GET'])
def admin_dashboard():
    email_filter = request.args.get('email')
    role_filter = request.args.get('role')
    date_filter = request.args.get('registration_date')

    query = User.query
    if email_filter:
        query = query.filter_by(email=email_filter)
    if role_filter:
        query = query.filter_by(role=role_filter)
    if date_filter:
        query = query.filter_by(registration_date=date_filter)

    users = query.all()
    return render_template('admin_dashboard.html', users=users)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)