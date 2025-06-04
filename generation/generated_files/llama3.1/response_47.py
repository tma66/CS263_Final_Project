from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/preview/<filename>', methods=['GET'])
def preview_file(filename):
    filepath = os.path.join('files', filename)
    
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        return 'File not found.', 404
    
    try:
        with open(filepath, 'rb') as file:
            content_type = mimetypes.guess_type(filename)[0]
            return send_file(file, mimetype=content_type, attachment_filename=filename)
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
