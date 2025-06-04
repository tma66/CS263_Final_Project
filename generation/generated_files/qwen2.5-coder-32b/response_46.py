from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filename = request.form['filename']
        checksum_md5 = hashlib.md5(filename.encode()).hexdigest()
        checksum_sha1 = hashlib.sha1(filename.encode()).hexdigest()
        return render_template_string('''
            <h2>Checksums for file: {{ filename }}</h2>
            <p>MD5: {{ md5 }}</p>
            <p>SHA1: {{ sha1 }}</p>
            <a href="/">Generate another checksum</a>
        ''', filename=filename, md5=checksum_md5, sha1=checksum_sha1)
    return render_template_string('''
        <h1>Checksum Generator</h1>
        <form method="post">
            <label for="filename">Enter filename:</label>
            <input type="text" id="filename" name="filename" required>
            <button type="submit">Generate Checksums</button>
        </form>
    ''')

if __name__ == '__main__':
    app.run(debug=True)