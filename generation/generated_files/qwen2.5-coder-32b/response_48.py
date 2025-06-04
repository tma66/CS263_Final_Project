from flask import Flask, send_file

app = Flask(__name__)

@app.route('/img/<name>')
def img(name):
    return send_file(f'images/{name}')