from flask import Flask, request

app = Flask(__name__)

@app.route('/img')
def img():
    file_path = request.args.get('file')
    with open(file_path, 'rb') as f:
        return f.read()