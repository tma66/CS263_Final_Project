from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = ''
    if request.method == 'POST':
        url = request.form.get('url')
    return render_template_string('''
        <form method="post">
            Enter URL: <input type="text" name="url">
            <input type="submit" value="Submit">
        </form>
        {% if url %}
            <p>Entered URL: {{ url }}</p>
        {% endif %}
    ''', url=url)

if __name__ == '__main__':
    app.run(debug=True)