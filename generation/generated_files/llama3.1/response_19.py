from flask import Flask, render_template, request
from jinja2 import Template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_html = request.form['email']
        template = Template(email_html)
        rendered_email = template.render()
        return render_template('preview.html', email=rendered_email)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/email')
def get_email():
    email = 'Email: {{ email }}'
    return {'email': email}

**templates/index.html**
<form action="" method="post">
    <textarea name="email" rows="10" cols="60"></textarea>
    <input type="submit" value="Preview Email">
</form>

{{ rendered_email | safe }}

**templates/preview.html**
<pre>{{ email }}</pre>