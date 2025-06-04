from flask import Flask, redirect, abort

app = Flask(__name__)

@app.route('/redirect/<url>')
def redirect_invalid_url(url):
    if url.startswith('http://example.com/') or url.startswith('https://example.com/'):
        return redirect(url)
    else:
        abort(400)

if __name__ == '__main__':
    app.run(debug=True)