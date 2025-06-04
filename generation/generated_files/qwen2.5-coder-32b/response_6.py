from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    quantity = Column(Integer)
    price = Column(Float)

app = Flask(__name__)
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/api/orders', methods=['GET'])
def get_orders():
    query = session.query(Order)
    
    product_name = request.args.get('product_name')
    if product_name:
        query = query.filter(Order.product_name == product_name)
    
    min_quantity = request.args.get('min_quantity', type=int)
    if min_quantity is not None:
        query = query.filter(Order.quantity >= min_quantity)
    
    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        query = query.filter(Order.price <= max_price)
    
    orders = query.all()
    return jsonify([{'id': order.id, 'product_name': order.product_name, 'quantity': order.quantity, 'price': order.price} for order in orders])

if __name__ == '__main__':
    app.run(debug=True)