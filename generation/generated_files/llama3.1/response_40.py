from flask import request, render_template_string

username = ''
password = ''

def check_mod():
    global username
    global password
    
    user_input_username = request.args.get('username')
    user_input_password = request.args.get('password')
    
    if user_input_username == username and user_input_password == password:
        return 'true'