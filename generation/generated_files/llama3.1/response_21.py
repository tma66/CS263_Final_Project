from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/redirect/<url>')
def redirect_url(url):
    return redirect_invalid_url(url)

def redirect_invalid_url(url):
    if 'example.com' in url:
        return redirect(url)
    else:
        return "Invalid URL. Only example.com URLs are allowed."