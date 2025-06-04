from flask import Flask, request, jsonify

app = Flask(__name__)

def calculate_tax(amount):
    tax_rate = 0.08  # default tax rate is 8%
    return amount * tax_rate

def calculate_interest(principal, rate, time):
    interest = principal * (1 + rate) ** time
    return interest

def generate_invoice(customer_name, invoice_date, total_amount):
    return {
        "customer": customer_name,
        "date": invoice_date,
        "amount": total_amount
    }

@app.route('/tax', methods=['POST'])
def process_tax():
    data = request.json
    if 'amount' in data:
        try:
            amount = float(data['amount'])
            tax = calculate_tax(amount)
            return jsonify({'tax': tax})
        except ValueError:
            return jsonify({'error': 'Invalid input'}), 400
    else:
        return jsonify({'error': 'Missing required field: amount'}), 400

@app.route('/interest', methods=['POST'])
def process_interest():
    data = request.json
    if 'principal' in data and 'rate' in data and 'time' in data:
        try:
            principal = float(data['principal'])
            rate = float(data['rate']) / 100
            time = int(data['time'])
            interest = calculate_interest(principal, rate, time)
            return jsonify({'interest': interest})
        except ValueError:
            return jsonify({'error': 'Invalid input'}), 400
    else:
        return jsonify({'error': 'Missing required fields: principal, rate, and time'}), 400

@app.route('/invoice', methods=['POST'])
def process_invoice():
    data = request.json
    if 'customer_name' in data and 'invoice_date' in data and 'total_amount' in data:
        try:
            customer_name = data['customer_name']
            invoice_date = data['invoice_date']
            total_amount = float(data['total_amount'])
            invoice = generate_invoice(customer_name, invoice_date, total_amount)
            return jsonify(invoice), 200
        except ValueError:
            return jsonify({'error': 'Invalid input'}), 400
    else:
        return jsonify({'error': 'Missing required fields: customer_name, invoice_date, and total_amount'}), 400

if __name__ == '__main__':
    app.run(debug=True)