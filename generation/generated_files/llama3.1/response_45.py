from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/download/<string:name>', methods=['GET'])
def download(name):
    path = 'documents/'
    if not os.path.isfile(path + name):
        return "File does not exist"
    else:
        return send_from_directory(path, name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)