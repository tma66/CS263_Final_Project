from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        try:
            response = requests.get(url)
            content = response.text[:1000]  # Preview first 1000 characters
        except Exception as e:
            content = f"Error fetching URL: {e}"
        return render_template_string('<pre>{{ content }}</pre>', content=content)
    return '''
        <form method="post">
            URL: <input type="text" name="url"><br>
            <input type="submit" value="Fetch">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)