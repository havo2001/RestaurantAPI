from app import app, db
from flask import request, jsonify, abort, url_for
from app.models import User


# Registration
@app.route('/api/users', methods=['POST'])
def new_user():
    data = request.get_json()
    if data['username'] is None or data['password'] is None or data['email'] is None:
        abort(400)  # missing arguments

    check_username = User.query.filter_by(username=data['username']).first()
    check_email = User.query.filter_by(email=data['email']).first()
    if check_username is not None or check_email is not None:
        abort(400)
        # existing user and email was registered
    # adding new user
    user = User(username=data['username'], email=data['email'], bonus=0)
    user.hash_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username, 'email': user.email, 'bonus': user.bonus}), 201, {
        'Location': url_for('get_user', id=user.id, _external=True)}


@app.route('/api/users/<int:id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username': user.username, 'email': user.email, 'bonus': user.bonus})
