from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database for demonstration purposes
database = {
    "users": ["user1@example.com", "user2@example.com"]
}

@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')
    
    if email in database["users"]:
        database["users"].remove(email)
        return jsonify({"message": f"User {email} has been unsubscribed."}), 200
    else:
        return jsonify({"message": "This user is not subscribed."}), 404

if __name__ == '__main__':
    app.run(debug=True)