from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database. It will be created if it doesn't exist.
conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Create table
cursor.execute('''CREATE TABLE IF NOT EXISTS orders
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   customer_name TEXT, order_date DATE, total REAL)''')

@app.route('/orders', methods=['GET'])
def get_orders():
    filters = request.args.to_dict()
    query = """
        SELECT *
        FROM orders"""
    
    if 'customer_name' in filters:
        query += " WHERE customer_name LIKE :name"
        
    if 'order_date' in filters:
        if '?' in filters['order_date']:
            query += " AND order_date BETWEEN :start AND :end"
        else:
            query += " AND order_date = :date"

    params = {}
    
    if 'customer_name' in filters:
        name = '%' + filters['customer_name'] + '%'
        params['name'] = name
        
    if 'order_date' in filters:
        if '?' in filters['order_date']:
            start, end = filters['order_date'].split('?')
            params['start'] = start
            params['end'] = end
        else:
            params['date'] = filters['order_date']

    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    orders = []
    for row in rows:
        orders.append({
            'id': row[0],
            'customer_name': row[1],
            'order_date': row[2],
            'total': row[3]
        })
        
    return jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)