import os


class Config(object):
    SECRET_KEY = 'Hello, my name is Ha'
    db_hostname = os.environ.get('POSTGRES_HOSTNAME')
    db_username = os.environ.get('POSTGRES_USERNAME')
    db_password = os.environ.get('POSTGRES_PASSWORD')
    db_database = os.environ.get('POSTGRES_DATABASE')
    db_port = os.environ.get('POSTGRES_PORT')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(db_username, db_password, db_hostname,
                                                                                 db_port, db_database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
