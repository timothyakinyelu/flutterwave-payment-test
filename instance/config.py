import os

class BaseConfig():
    """ Base configuration class."""
    
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_SORT_KEYS = False
    WTF_CSRF_ENABLED = True
    
    
class DevelopmentConfig(BaseConfig):
    """ Development environment configuration """
    
    DEBUG = os.environ.get('DEBUG')
    TEMPLATES_AUTO_RELOAD = True
    SEC_KEY = os.environ.get('SEC_KEY')
    MY_HASH = os.environ.get('MY_HASH')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
    

app_config = {
    'development': DevelopmentConfig
}