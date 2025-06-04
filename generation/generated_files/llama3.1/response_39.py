def check_mod():
    username = input("Enter username: ")
    password = input("Enter password: ")

    if username == "admin" and password == "password":
        return True
    else:
        return False