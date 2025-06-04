from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/<path:path>')
def get_file(path):
    img_dir = 'images/'
    if os.path.exists(img_dir + path):
        return send_from_directory(img_dir, path)
    else:
        return 'File not found'

if __name__ == '__main__':
    app.run()