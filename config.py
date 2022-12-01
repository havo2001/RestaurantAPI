class Config(object):
    SECRET_KEY = 'Hello, my name is Ha'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:150101@localhost:5432/restaurant'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
