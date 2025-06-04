from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        return render_template_string("<p>URL: {{ url }}</p>", url=url)
    else:
        return render_template_string('<form action="" method="post"><input type="text" name="url"><button type="submit">Submit</button></form>')

if __name__ == '__main__':
    app.run(debug=True)