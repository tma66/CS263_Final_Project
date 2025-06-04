from flask import Flask, request, send_from_directory, abort
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        abort(400, description="No file part")
    file = request.files['file']
    if file.filename == '':
        abort(400, description="No selected file")
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f"File {file.filename} uploaded successfully"

@app.route('/view')
def view_file():
    filename = request.args.get('filename')
    if not filename:
        abort(400, description="Filename parameter is required")
    if '..' in filename or os.path.isabs(filename):
        abort(403)
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)