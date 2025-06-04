from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Define path to project documents directory
docs_dir = '/path/to/project/docs'

@app.route('/project-documents', methods=['GET'])
def get_project_documents():
    documents = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
    return jsonify({'documents': documents})

if __name__ == '__main__':
    app.run(debug=True)