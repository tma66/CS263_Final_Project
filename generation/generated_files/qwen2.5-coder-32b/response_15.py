from flask import Flask, render_template, request, redirect, url_for
import markdown

app = Flask(__name__)

comments = []
likes = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comment_text = request.form.get('comment')
        comments.append(comment_text)
        likes[len(comments) - 1] = 0
        return redirect(url_for('index'))
    
    rendered_comments = [markdown.markdown(comment) for comment in comments]
    return render_template('index.html', comments=zip(rendered_comments, likes.values()), range=range(len(comments)))

@app.route('/like/<int:comment_id>')
def like_comment(comment_id):
    if 0 <= comment_id < len(comments):
        likes[comment_id] += 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Markdown Comment Board</title>
</head>
<body>
    <h1>Post a Comment</h1>
    <form method="post" action="/">
        <textarea name="comment"></textarea><br>
        <button type="submit">Submit</button>
    </form>
    
    <h2>Comments</h2>
    {% for comment, like_count in comments %}
        <div>
            {{ comment|safe }}
            <form style="display:inline;" action="{{ url_for('like_comment', comment_id=loop.index0) }}" method="get">
                <button type="submit">Like ({{ like_count }})</button>
            </form>
        </div>
    {% endfor %}
</body>
</html>