from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    email_content = ''
    if request.method == 'POST':
        email_content = request.form.get('email_content', '')
    return render_template('index.html', email_content=email_content)

if __name__ == '__main__':
    app.run(debug=True)

```
<!-- templates/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Email Preview</title>
</head>
<body>
    <h1>Write Your Email</h1>
    <form method="post">
        <textarea name="email_content" rows="20" cols="60">{{ email_content }}</textarea><br>
        <input type="submit" value="Preview Email">
    </form>
    <h2>Email Preview:</h2>
    <div style="border: 1px solid #ccc; padding: 10px;">
        {{ email_content|safe }}
    </div>
</body>
</html>
```