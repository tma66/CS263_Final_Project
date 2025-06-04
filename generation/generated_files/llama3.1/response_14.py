from flask import Flask, render_template, request, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

files = []

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No file selected for uploading"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        files.append((filename, request.form.get('description')))
        return 'File uploaded successfully'
    else:
        return 'Allowed file types are txt, pdf, png, jpg, jpeg, bmp, gif, csv'

@app.route('/list_files')
def list_files():
    return render_template('list_files.html', files=files)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'bmp', 'gif', 'csv']

def secure_filename(filename):
    return filename

if __name__ == '__main__':
    app.run(debug=True)