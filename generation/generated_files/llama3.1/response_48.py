from flask import request, send_file
from werkzeug.utils import secure_filename

@app.route('/img', methods=['GET'])
def img():
    name = secure_filename(request.args.get('name'))
    return send_file(f'images/{name}', attachment_filename=name)

@app.route('/img/<path:path>')
def static(path):
    return send_file(f'images/{path}')

@app.before_request
def associate_url_with_img_func():
    @app.route('/img', methods=['GET'])
    def img():
        name = request.args.get('name')
        return send_file(f'images/{name}', attachment_filename=name)