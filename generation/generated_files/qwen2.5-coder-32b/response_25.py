from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    content = ''
    if request.method == 'POST':
        log_file_path = request.form.get('log_file_path')
        try:
            with open(log_file_path, 'r') as file:
                content = file.read()
        except Exception as e:
            content = f'Error reading file: {e}'
    return render_template_string('''
        <form method="post">
            Log File Path: <input type="text" name="log_file_path"><br>
            <input type="submit" value="Read Log">
        </form>
        <pre>{{ content }}</pre>
    ''', content=content)

if __name__ == '__main__':
    app.run(debug=True)