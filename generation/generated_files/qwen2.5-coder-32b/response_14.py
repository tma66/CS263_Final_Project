from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
)
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        description = request.form.get("description")
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            with open("descriptions.txt", "a") as f:
                f.write(f"{filename}:{description}\n")
            return redirect(url_for("index"))
    files = []
    if os.path.exists("descriptions.txt"):
        with open("descriptions.txt", "r") as f:
            for line in f:
                filename, description = line.strip().split(":", 1)
                files.append((filename, description))
    return render_template("index.html", files=files)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)
