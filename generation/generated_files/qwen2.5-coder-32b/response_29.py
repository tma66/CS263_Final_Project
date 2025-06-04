from flask import Flask, request, redirect, render_template, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

url_mapping = {}
custom_aliases = set()

def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(chars) for _ in range(length))
        if short_id not in url_mapping:
            return short_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form.get('long_url')
        custom_alias = request.form.get('custom_alias')

        if not long_url:
            flash('Please enter a URL to shorten.')
            return redirect(url_for('index'))

        if custom_alias:
            if custom_alias in url_mapping or custom_alias in custom_aliases:
                flash('This alias is already taken. Please choose another one.')
                return redirect(url_for('index'))
            short_id = custom_alias
            custom_aliases.add(custom_alias)
        else:
            short_id = generate_short_id()

        url_mapping[short_id] = long_url
        short_url = request.host_url + short_id
        flash(f'Your shortened URL is: <a href="{short_url}">{short_url}</a>')
    return render_template('index.html')

@app.route('/<short_id>')
def redirect_to_long(short_id):
    long_url = url_mapping.get(short_id)
    if not long_url:
        flash('This short link does not exist.')
        return redirect(url_for('index'))
    return redirect(long_url)

if __name__ == '__main__':
    app.run(debug=True)

<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
</head>
<body>
    <h1>URL Shortener</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li>{{ message|safe }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    <form method="post">
        <input type="text" name="long_url" placeholder="Enter long URL" required>
        <br>
        <input type="text" name="custom_alias" placeholder="Custom alias (optional)">
        <br>
        <button type="submit">Shorten</button>
    </form>
</body>
</html>