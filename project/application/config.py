import os 
basedir=os.path.abspath(os.path.dirname(__file__))

class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "pdb.sqlite3")
    DEBUG = True   
    #during production always read the security key from the os env.
    SECRET_KEY = "75fu537284676f387th" #Strong key
    SECURITY_REGISTERABLE = True 
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_UNAUTHORIZED_VIEW=None


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DEBUG = True   
    #during production always read the security key from the os env.
    SECRET_KEY = "75fu537284676f387th" #Strong key
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "reallydssfrrv"
    SECURITY_REGISTERABLE = True 
    SECURITY_SEND_REGISTER_EMAIL=False
    SECURITY_UNAUTHORIZED_VIEW=None
    WTF_CSRF_ENABLED=False