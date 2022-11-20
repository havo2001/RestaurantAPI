from flask import jsonify
from app import app
from app.api.auth import auth, g

@app.route('/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

