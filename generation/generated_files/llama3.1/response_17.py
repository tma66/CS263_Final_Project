from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        return render_template_string(
            '''
            <html>
                <body>
                    <h1>URL: {{ url }}</h1>
                </body>
            </html>
            ''',
            url=url
        )
    else:
        return render_template_string(
            '''
            <html>
                <body>
                    <form method="POST">
                        <input type="text" name="url" placeholder="Enter URL">
                        <button type="submit">Submit</button>
                    </form>
                </body>
            </html>
            '''
        )

if __name__ == '__main__':
    app.run(debug=True)