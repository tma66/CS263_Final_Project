from flask import Flask, render_template, request
from jinja2 import Template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subject = request.form['subject']
        body = request.form['body']
        template = Template('''
            <html>
                <head></head>
                <body>
                    <h1>{{ subject }}</h1>
                    {{ body|safe }}
                </body>
            </html>
        ''')
        rendered_email = template.render(subject=subject, body=body)
        return render_template('preview.html', email=rendered_email)

    return render_template('index.html')

@app.route('/preview/<email>')
def preview(email):
    return render_template_string(f'''
        <html>
            <head></head>
            <body>
                {{ email|safe }}
            </body>
        </html>
    ''', email=email)

if __name__ == '__main__':
    app.run(debug=True)