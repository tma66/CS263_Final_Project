def check_mod():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == 'correct_username' and password == 'correct_password':
        return 'true'
    else:
        return 'false'