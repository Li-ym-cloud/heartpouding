import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or '!@#$1231ADA'

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URL = f"""
    postgresql+psycogp2://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_HOST')}:5432/{os.environ.get('DB_NAME')}
    """

config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}