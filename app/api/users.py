from app import app, db
from flask import request, jsonify, abort, url_for
from app.models import User
from app.api.errors import bad_request
from app.api.auth import auth, g

# Index page
@app.route('/', methods=['GET'])
def home():
    return jsonify("hello")


# Home page
@app.route('/users/login', methods=['GET'])
@auth.login_required()
def login():
    return jsonify({'username': g.user.username, 'email': g.user.email, 'bonus': g.user.bonus}), 201, {
        'Location': url_for('get_user', id=g.user.id, _external=True)}


# Get the information of user
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return bad_request('This id has been not registered')
    return jsonify({'username': user.username, 'email': user.email, 'bonus': user.bonus})


# Registration
@app.route('/users', methods=['POST'])
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


# Update user, change the email or password:
@app.route('/users/<int:id>', methods=['PUT'])
@auth.login_required
def update_user(id):
    if g.user.id != id:
        abort(403)
    user = User.query.get(id)
    data = request.get_json()
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('This email has been registered, please use another email')

    if 'email' in data:
        user.email = data['email']

    if 'password' in data:
        user.hash_password(data['password'])
    db.session.commit()
    return jsonify({'data': 'Your information has been updated'})

