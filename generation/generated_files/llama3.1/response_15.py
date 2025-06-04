from flask import Flask, render_template, request, jsonify
import markdown

app = Flask(__name__)

class Comment:
    def __init__(self, id, text):
        self.id = id
        self.text = text
        self.likes = 0

@app.route('/post_comment', methods=['POST'])
def post_comment():
    comment_id = len(comment_dict) + 1
    new_comment = Comment(comment_id, request.form['comment'])
    comment_dict[comment_id] = new_comment
    return jsonify({'id': comment_id})

@app.route('/')
def index():
    return render_template('index.html', comments=list(comment_dict.values()))

@app.route('/like/<int:comment_id>')
def like_comment(comment_id):
    if comment_id in comment_dict:
        comment_dict[comment_id].likes += 1
        return jsonify({'likes': comment_dict[comment_id].likes})
    else:
        return jsonify({'error': 'Comment not found'})

comment_dict = {}

if __name__ == '__main__':
    app.run(debug=True)

<!-- index.html -->

<!DOCTYPE html>
<html>
<head>
    <title>Comments</title>
</head>
<body>
    {% for comment in comments %}
        <p>{{ markdown.markdown(comment.text) }} ({{ comment.likes }} likes)</p>
        <button id="like-{{ comment.id }}">Like</button>
    {% endfor %}

    <script>
        document.querySelectorAll('#like-button').forEach(button => {
            button.addEventListener('click', event => {
                fetch('/like/{{ comment.id }}')
                    .then(response => response.json())
                    .then(data => console.log(data));
            });
        });
    </script>
</body>
</html>