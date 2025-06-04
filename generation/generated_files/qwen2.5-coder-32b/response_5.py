from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financial_app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    accounts = db.relationship('Account', backref='user', lazy=True)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    recipient_account_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    return jsonify({'message': 'Login successful'}), 200

@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    sender_account = Account.query.get(data['sender_account_id'])
    recipient_account = Account.query.get(data['recipient_account_id'])
    if not sender_account or not recipient_account:
        return jsonify({'message': 'Invalid account'}), 404
    if sender_account.balance < data['amount']:
        return jsonify({'message': 'Insufficient balance'}), 403
    sender_account.balance -= data['amount']
    recipient_account.balance += data['amount']
    new_transaction = Transaction(account_id=sender_account.id, amount=data['amount'], recipient_account_id=recipient_account.id)
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify({'message': 'Transfer successful'}), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)