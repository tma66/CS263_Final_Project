from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/images/<filename>')
def serve_image(filename):
    if os.path.exists(os.path.join('images', filename)):
        return send_from_directory('images', filename)
    else:
        return "File not found", 404