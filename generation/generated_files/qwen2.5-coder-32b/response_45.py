from flask import Flask, send_from_directory, abort

app = Flask(__name__)
DOWNLOAD_FOLDER = '/path/to/documents'

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_from_directory(DOWNLOAD_FOLDER, filename)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)