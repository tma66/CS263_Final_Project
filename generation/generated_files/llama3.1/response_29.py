import random
import string
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for simplicity; consider using a database in production
short_urls = {}

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/url', methods=['POST'])
def shorten_url():
    data = request.json
    if 'url' not in data or ('alias' in data and not isinstance(data['alias'], str)):
        return jsonify({'error': 'Invalid request'}), 400

    url = data['url']
    alias = data.get('alias')

    if alias:
        if alias in short_urls:
            return jsonify({'error': 'Alias already exists'}), 409
        short_code = alias
    else:
        short_code = generate_short_code()

    short_urls[short_code] = url

    return jsonify({'short_url': f'http://localhost:5000/{short_code}'}), 201

@app.route('/<string:code>')
def redirect(code):
    if code in short_urls:
        return jsonify({'redirect_url': short_urls[code]}), 302
    else:
        return jsonify({'error': 'Short URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)