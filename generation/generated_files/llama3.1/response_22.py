from flask import Flask, url_for, request, redirect, render_template

app = Flask(__name__)

@app.route('/redirect/<url>')
def redirect_invalid_url(url):
    if 'example.com' in url:
        return redirect(url)
    else:
        return "Error: URL is not from example.com domain"