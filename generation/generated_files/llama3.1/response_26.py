from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            response = requests.get(url)
            content_type = response.headers.get('Content-Type')
            if 'image' in content_type or 'video' in content_type:
                return render_template_string(
                    '<img src="data:{};base64,{}" style="width:100px">'.format(
                        content_type.split(';')[0].split(':')[1],
                        response.content.decode('utf-8')
                    )
                )
            elif 'text/html' in content_type or 'application/json' in content_type:
                return render_template_string(
                    '<pre>{}</pre>'.format(response.text)
                )
        except Exception as e:
            return str(e)

    return '''
    <html>
      <body>
        <h1>Upload your file</h1>
        <form action="" method="post" enctype="multipart/form-data">
          <input type="text" name="url">
          <input type="submit" value="Submit request">
        </form>
      </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)