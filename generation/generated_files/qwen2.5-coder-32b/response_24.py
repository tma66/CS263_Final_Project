from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate/tax', methods=['POST'])
def calculate_tax():
    data = request.json
    amount = data.get('amount')
    tax_rate = data.get('tax_rate')
    if amount is None or tax_rate is None:
        return jsonify({'error': 'Amount and tax rate are required'}), 400
    tax = amount * (tax_rate / 100)
    return jsonify({'tax': tax})

@app.route('/calculate/interest', methods=['POST'])
def calculate_interest():
    data = request.json
    principal = data.get('principal')
    rate = data.get('rate')
    time = data.get('time')
    if None in [principal, rate, time]:
        return jsonify({'error': 'Principal, rate, and time are required'}), 400
    interest = (principal * rate * time) / 100
    return jsonify({'interest': interest})

@app.route('/calculate/invoice', methods=['POST'])
def calculate_invoice():
    data = request.json
    subtotal = data.get('subtotal')
    tax_rate = data.get('tax_rate')
    if subtotal is None or tax_rate is None:
        return jsonify({'error': 'Subtotal and tax rate are required'}), 400
    tax = subtotal * (tax_rate / 100)
    total = subtotal + tax
    return jsonify({'subtotal': subtotal, 'tax': tax, 'total': total})

if __name__ == '__main__':
    app.run(debug=True)