import os


# default config
class BaseConfig(object):
    DEBUG = False
    # shortened for readability
    SECRET_KEY = 'super secret string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/prixma/Desktop/TP-Pratica_Software/pds2020-2/backend/migrations/MyRecipes.db'#os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    ECRET_KEY = 'super secret string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False