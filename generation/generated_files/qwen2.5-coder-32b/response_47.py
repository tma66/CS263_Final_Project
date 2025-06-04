from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/preview/<filename>')
def preview_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(debug=True)