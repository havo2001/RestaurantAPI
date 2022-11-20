from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    bonus = db.Column(db.Integer)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_id = db.Column(db.Integer)
    username = db.Column(db.String(64))
    status = db.Column(db.String(64))
    date_order = db.Column(db.String)  # "%d-%m-%Y"
    added_note = db.Column(db.String)

    @property
    def serialize(self):
        return {
            'table_id': self.id,
            'username': self.username,
            'date_order': self.date_order,
            'note': self.added_note
        }




