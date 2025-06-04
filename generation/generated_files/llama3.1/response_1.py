from flask import redirect, url_for, request
from db_operations import insert_user_message_in_db

def post():
    username = request.form['username']
    message = request.form['message']
    insert_user_message_in_db(username, message)
    return redirect(url_for('main'))

@app.route('/show_messages')
def show_messages():
    messages = select_user_messages_from_db()
    return render_template('messages.html', messages=messages)