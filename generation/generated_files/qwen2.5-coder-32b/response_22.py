from flask import Flask, request, redirect, abort

app = Flask(__name__)

@app.route('/redirect/<path:url>')
def redirect_invalid_url(url):
    if 'example.com' in url:
        return redirect(url)
    else:
        abort(400, description="Invalid URL")

if __name__ == '__main__':
    app.run(debug=True)