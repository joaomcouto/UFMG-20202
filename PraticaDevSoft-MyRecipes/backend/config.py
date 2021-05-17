import os


# default config
class BaseConfig(object):
    DEBUG = True
    # shortened for readability
    SECRET_KEY = 'super secret string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///MyRecipes.db'#os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_LIFESPAN = {'hours' : 24}
    JWT_REFRESH_LIFESPAN = {'days' : 30}
    UPLOAD_FOLDER = '../uploads'


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    ECRET_KEY = 'super secret string'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False