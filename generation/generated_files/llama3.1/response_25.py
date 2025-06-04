from flask import Flask, request, render_template
import logging
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        log_file_path = request.form.get('log_file_path')
        try:
            with open(log_file_path, 'r') as file:
                logs = file.readlines()
                return render_template('index.html', logs=logs)
        except FileNotFoundError:
            error_message = f"Log file not found at path: {log_file_path}"
            return render_template('index.html', error_message=error_message)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/logs/<path:path>')
def view_logs(path):
    try:
        with open(path, 'r') as file:
            logs = file.readlines()
            return render_template('view_logs.html', path=path, logs=logs)
    except FileNotFoundError:
        error_message = f"Log file not found at path: {path}"
        return render_template('error.html', error_message=error_message)

@app.route('/view/<int:start_line>_<int:end_line>')
def view_log_range(start_line, end_line):
    try:
        with open(request.args.get('path'), 'r') as file:
            logs = [line.strip() for line in file.readlines()]
            start_index = max(0, start_line-1)
            end_index = min(len(logs), end_line)
            return render_template('view_log_range.html', path=request.args.get('path'), logs=logs[start_index:end_index])
    except FileNotFoundError:
        error_message = f"Log file not found at path: {request.args.get('path')}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)