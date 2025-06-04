from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/file_contents', methods=['POST'])
def file_contents():
    data = request.json
    filename = data.get('filename')
    try:
        with open(filename, 'r') as file:
            contents = file.read()
            return jsonify({'filename': filename, 'contents': contents})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)