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

    # This might introduce a RCE-Vulnerability, so don't actually use this until this notice is revoked
    # Don't even set the environment variables, I beg you. It will lead to disaster.
    # To enable, set environment variable to True or any other value
    ENABLE_TELEGRAM_INTEGRATION = os.environ.get('ENABLE_TELEGRAM_INTEGRATION') or False
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or None
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or None
