from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    html_content = ''
    if request.method == 'POST':
        html_content = request.form.get('html_content', '')
    return render_template('index.html', html_content=html_content)

if __name__ == '__main__':
    app.run(debug=True)

<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Preview</title>
</head>
<body>
    <h1>Write Your Email in HTML</h1>
    <form method="post">
        <textarea name="html_content" rows="20" cols="80">{{ html_content }}</textarea><br>
        <input type="submit" value="Preview">
    </form>
    <h2>Email Preview:</h2>
    <iframe srcdoc="{{ html_content|safe }}" style="width:100%; height:500px;"></iframe>
</body>
</html>