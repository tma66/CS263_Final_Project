from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__)
PROJECT_DOCS_FOLDER = '/path/to/project/docs'

@app.route('/documents/<filename>', methods=['GET'])
def get_document(filename):
    if filename in os.listdir(PROJECT_DOCS_FOLDER):
        return send_from_directory(PROJECT_DOCS_FOLDER, filename)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)