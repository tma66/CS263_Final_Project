from flask import Flask, render_template, request, redirect

app = Flask(__name__)

user_profiles = {
    '1': {'bio': 'Hello, I am a user!'}
}

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if request.method == 'POST':
        new_bio = request.form['bio']
        user_profiles[user_id]['bio'] = new_bio
        return redirect(f'/profile/{user_id}')
    bio = user_profiles.get(user_id, {}).get('bio', '')
    return render_template('profile.html', user_id=user_id, bio=bio)

if __name__ == '__main__':
    app.run(debug=True)