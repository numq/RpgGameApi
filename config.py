import base64
import os

from app.utilities import constants

basedir = os.path.abspath(os.path.dirname(__file__)) + f'{constants.DATABASE_PACKAGE}'
basedir_test = os.path.abspath(os.path.dirname(__file__)) + f'{constants.DATABASE_PACKAGE_TEST}'
main_db = os.path.join(basedir, 'db.sqlite')
test_db = os.path.join(basedir_test, 'test.sqlite')


class Config:
    DEBUG = True
    TESTING = True
    SECRET_KEY = base64.b64encode(os.urandom(64)).decode('utf-8')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_BINDS = {
        'db': 'sqlite:///' + main_db,
        'test': 'sqlite:///' + test_db
    }


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, main_db)


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, test_db)
