from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello_world():
    name = request.args.get('name')
    if name is None:
        return "Hello, World!"
    else:
        return f"Hello, {name}!"

if __name__ == '__main__':
    app.run(debug=True)