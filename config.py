import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_POOL_RECYCLE = 30
    SQLALCHEMY_POOL_TIMEOUT = 5
    SQLALCHEMY_PRE_PING = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': SQLALCHEMY_POOL_RECYCLE,
        'pool_timeout': SQLALCHEMY_POOL_TIMEOUT,
        'pool_pre_ping': SQLALCHEMY_PRE_PING
    }
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set this value to reserve some features for admins only. Only use this if you serve your website exclusively
    # over HTTPS. Cookies will get leaked otherwise.
    MANAGEMENT_PASSWORD = os.environ.get('MANAGEMENT_PASSWORD') or None

    # Webhook Integration
    # To enable, set environment variable ENABLE_WEBHOOK_INTEGRATION to True or any other value
    ENABLE_WEBHOOK_INTEGRATION = os.environ.get('ENABLE_WEBHOOK_INTEGRATION') or False
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL') or None
    WEBHOOK_AUTHORIZATION_BEARER = os.environ.get('WEBHOOK_AUTHORIZATION_BEARER') or None

    # This might introduce a RCE-Vulnerability, so don't actually use this until this notice is revoked
    # Don't even set the environment variables, I beg you. It will lead to disaster.
    # To enable, set environment variable ENABLE_TELEGRAM_INTEGRATION to True or any other value
    ENABLE_TELEGRAM_INTEGRATION = os.environ.get('ENABLE_TELEGRAM_INTEGRATION') or False
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or None
    TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID') or None
