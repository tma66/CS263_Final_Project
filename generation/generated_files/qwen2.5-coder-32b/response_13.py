from flask import Flask, render_template, request

app = Flask(__name__)

comments = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment = request.form.get('comment')
        if comment:
            comments.append(comment)
    return render_template('index.html', comments=comments)

if __name__ == '__main__':
    app.run(debug=True)

<!-- templates/index.html -->
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Comments</title>
</head>
<body>
    <h1>Submit a Comment</h1>
    <form method="post">
        <textarea name="comment" rows="4" cols="50"></textarea><br>
        <input type="submit" value="Submit">
    </form>
    <h2>Comments:</h2>
    <ul>
        {% for comment in comments %}
            <li>{{ comment }}</li>
        {% endfor %}
    </ul>
</body>
</html>