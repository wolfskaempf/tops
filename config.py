import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set this value to reserve some features for admins only. Only use this if you serve your website exclusively
    # over HTTPS. Cookies will get leaked otherwise.
    MANAGEMENT_PASSWORD = os.environ.get('MANAGEMENT_PASSWORD') or None
