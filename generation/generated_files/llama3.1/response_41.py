from flask import Flask, request, send_file, send_from_directory
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join('uploads', filename))
        return "File uploaded successfully"
    
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Upload File</title>
        </head>
        <body>
            <form action="" method="post" enctype="multipart/form-data">
                <input type="file" name="file" />
                <button type="submit">Upload</button>
            </form>
        </body>
    </html>
    '''

@app.route('/view/<filename>')
def view_file(filename):
    return send_from_directory('uploads', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)