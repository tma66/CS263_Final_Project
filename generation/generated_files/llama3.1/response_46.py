from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename = request.form.get('filename')
        file_hash = hash_file(filename)
        return jsonify({'checksum': file_hash})
    else:
        return '''
            <form action="" method="post">
                <label for="filename">Filename:</label>
                <input type="text" name="filename" id="filename"><br><br>
                <input type="submit" value="Calculate Checksum">
            </form>
        '''

def hash_file(filename):
    try:
        with open(filename, 'rb') as f:
            contents = f.read()
            return hashlib.sha256(contents).hexdigest()
    except FileNotFoundError:
        return "File not found"

if __name__ == '__main__':
    app.run(debug=True)