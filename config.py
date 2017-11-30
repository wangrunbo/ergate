class DefaultConfig(object):
    # App
    DEBUG = False
    BCRYPT_LEVEL = 13

    # Session
    SECRET_KEY = '\x1b\xae\xa6\xe2\x97\t\xe4\\\x12v\xf6B\x1a!E\xd5\xdcL\xb3T\xe6?\xd9\xec'
    PERMANENT_SESSION_LIFETIME = 3600

    # TODO DataResource
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_ECHO = False

    # Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    MAIL_MAX_EMAILS = None

    # Config
    TOKEN_SALT = 'QokRn0cWdaYyF9HWGDFKssHPjSJhaBZ5mdS-U3eCwt2OLphVTKz7BUrsjPjenUy88wLnojITvX-EDR3FCyjA'


class DevelopConfig(DefaultConfig):
    """
    開発環境
    """
    # App
    DEBUG = True

    # TODO DataResource
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456aaa@127.0.0.1:3306/hunter?charset=utf8"
    # SQLALCHEMY_ECHO = True


class ProductionConfig(DefaultConfig):
    """
    本番環境
    """
    # App
    DEBUG = False
    SECRET_KEY = 'h\x88\x12-\xf3\xc1z\xa9\x17\xd5\xfb\x82P?\xb7o\xd8)\x08\x85\x94[=\x99'

    # TODO DataResource
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/hunter?charset=utf8"
    # SQLALCHEMY_ECHO = False
