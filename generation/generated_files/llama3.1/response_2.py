import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')
    
    if db_user(email):
        delete_user_from_db(email)
        unsubscribe_from_mailing_list(email)
        return 'User unsubscribed successfully'
    else:
        return 'You are not subscribed'

def db_user(email):
    # assuming db_connection is a function that returns a database connection
    with db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        return bool(cur.fetchone())

def delete_user_from_db(email):
    with db_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE email = ?", (email,))

def unsubscribe_from_mailing_list(email):
    # assuming api_key is a constant or variable that contains the API key
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.delete(f'https://api.mailinglist.com/{email}', headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False

if __name__ == '__main__':
    app.run(debug=True)