from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/filenames', methods=['POST'])
def handle_post_request():
    data = request.json
    if 'filename' not in data:
        return jsonify({'error': 'Missing filename'}), 400
    
    try:
        with open(data['filename'], 'r') as file:
            contents = file.read()
            return jsonify({'contents': contents}), 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)