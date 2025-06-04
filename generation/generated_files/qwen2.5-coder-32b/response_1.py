from flask import request, redirect, url_for, render_template

def post():
    username = request.form.get('username')
    message = request.form.get('message')
    insert_user_message_in_db(username, message)
    return redirect(url_for('main_page'))

@app.route('/main_page')
def main_page():
    messages = get_messages_from_db()
    return render_template('main_page.html', messages=messages)