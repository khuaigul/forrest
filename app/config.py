import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = '537635a91d8d7769ff6a355759e1d2949bc3ce25'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'forrest.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False