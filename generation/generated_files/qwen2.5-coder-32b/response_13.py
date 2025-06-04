from flask import Flask, render_template, request

app = Flask(__name__)

comments = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        comment = request.form.get("comment")
        if comment:
            comments.append(comment)
    return render_template("index.html", comments=comments)


if __name__ == "__main__":
    app.run(debug=True)
