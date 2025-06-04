from flask import Flask, render_template, request
import json

app = Flask(__name__)

# In-memory storage for users' bios
users_bios = {}

@app.route('/')
def index():
    return 'Welcome to the Profile Page'

@app.route('/profile/<username>')
def profile(username):
    if username in users_bios:
        return render_template('profile.html', bio=users_bios[username])
    else:
        return 'User not found', 404

@app.route('/edit_bio/<username>', methods=['GET', 'POST'])
def edit_bio(username):
    if request.method == 'POST':
        new_bio = request.form['bio']
        users_bios[username] = new_bio
        return redirect(url_for('profile', username=username))
    else:
        return render_template('edit.html')

if __name__ == '__main__':
    app.run(debug=True)

# profile.html template
{% extends "base.html" %}

{% block content %}
  <h1>{{ username }}'s Profile</h1>
  <p>Bio: {{ bio }}</p>
  <form action="{{ url_for('edit_bio', username=username) }}" method="post">
    <textarea name="bio">{{ users_bios[username] }}</textarea>
    <input type="submit" value="Save Changes">
  </form>
{% endblock %}

# edit.html template
{% extends "base.html" %}

{% block content %}
  <h1>Edit Bio</h1>
  <form action="{{ url_for('edit_bio', username=username) }}" method="post">
    <textarea name="bio">{{ users_bios[username] }}</textarea>
    <input type="submit" value="Save Changes">
  </form>
{% endblock %}